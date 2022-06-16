import sys
import argparse
import uuid
from typing import Optional

import txaio
from txaio import time_ns

txaio.use_twisted()

from twisted.internet import reactor
from twisted.internet.error import ReactorNotRunning
from twisted.internet.defer import inlineCallbacks

from autobahn.util import hltype, hlval
from autobahn.wamp import cryptosign
from autobahn.wamp.types import CloseDetails, EventDetails
from autobahn.wamp.exception import ApplicationError
from autobahn.twisted.util import sleep
from autobahn.twisted.wamp import ApplicationSession, ApplicationRunner


class ExampleClient(ApplicationSession):

    def __init__(self, config=None):
        self.log.info('{func} initializing component: {config}', func=hltype(self.__init__), config=config)
        super().__init__(config)
        try:
            self._key = cryptosign.CryptosignKey.from_file(config.extra['key'])
        except Exception as e:
            self.log.error(
                'could not load client private key: {log_failure}', log_failure=e)
            raise
        else:
            self.log.info('client key loaded: {pubkey}', pubkey=hlval(self._key.public_key()))

    def onConnect(self):
        self.log.info('{func} connected to router', func=hltype(self.onConnect))
        try:
            authid = self.config.extra['authid']
            authextra = {
                'pubkey': self._key.public_key(),
                'channel_binding': None,
            }
            self.join(self.config.realm,
                      authmethods=['cryptosign'],
                      # authid may bee None for WAMP-cryptosign!
                      authid=authid,
                      authextra=authextra)
        except Exception as e:
            self.log.error('could not join realm: {log_failure}', log_failure=e)
            raise

    def onChallenge(self, challenge):
        self.log.info('{func} authentication challenge received: {challenge}',
                      func=hltype(self.onChallenge), challenge=challenge)

        signed_challenge = self._key.sign_challenge(self, challenge, channel_id_type=None)

        return signed_challenge

    @inlineCallbacks
    def onJoin(self, session_details):
        self.log.info('{func} session joined:\n{details}', func=hltype(self.onJoin), details=session_details)

        if False:
            for i in range(5):
                value = yield self.call('com.example.private.get_time')
                self.log.info('get_time(): {value}', value=hlval(value))
                yield sleep(.5)

            value = yield self.call('com.example.private.add2', 23, 666)
            self.log.info('add2(23, 666): {value}', value=hlval(value))

            t0 = txaio.time_ns()
            value = yield self.call('com.example.private.slow_square', 16, 0.5)
            t1 = txaio.time_ns()
            duration = (t1 - t0) / 10**6
            self.log.info('slow_square(16): {value} in {duration} ms', value=hlval(value), duration=hlval(duration))

            def on_message_changed(notification, event_details: Optional[EventDetails] = None):
                self.log.info('{func}: {notification}\n{details}',
                              func=hltype(on_message_changed),
                              notification=notification,
                              details=event_details)

            yield self.subscribe(on_message_changed, 'com.example.private.on_message_changed')

            value = yield self.call('com.example.private.set_message',
                                    'Der Räuber Hotzenplotz ist da! ({})'.format(t0))
            self.log.info('set_message(): {value}', value=hlval(value))

        # FIXME: wamp.error.invalid_argument: call result from procedure ...
        # clock_oid = uuid.UUID('ba3b1e9f-3006-4eae-ae88-cf5896b36342')
        # result = yield self.call('eth.pydefi.clock.{}.get_clock_address'.format(clock_oid))
        # self.log.info('get_clock_address(): {result}', result=hlval(result))

        replica_oid = uuid.UUID('ba3b1e9f-3006-4eae-ae88-cf5896b36342')
        book_oid = uuid.UUID('a17f0b45-1ed2-4b1a-9a7d-c112e8cd5d9b')
        period = {
            'period_dur': 12,
            'start_ts': txaio.time_ns(),
            'limit': 10,
        }
        procedure = 'com.example.private.replica.{}.book.{}.get_candle_history'.format(replica_oid, book_oid)

        # test case 1: test valid call
        if True:
            result = yield self.call(procedure, 12, txaio.time_ns())
            self.log.info('get_candle_history() - test case 1: {result}', result=hlval(result))

        # test case 2: test valid call with kwargs
        if False:
            result = yield self.call(procedure, 12, txaio.time_ns(), limit=100)
            self.log.info('get_candle_history() - test case 2: {result}', result=hlval(result))

        # test case 3: test call with invalid args length (too many)
        if False:
            try:
                yield self.call(procedure, 12, txaio.time_ns(), 'invalid additional argument')
            except Exception as e:
                if isinstance(e, ApplicationError) and e.error == 'wamp.error.invalid_argument':
                    if 'unexpected positional argument' not in e.args[0]:
                        raise RuntimeError('test case 3: did not find expected error text in exception!')
                    else:
                        self.log.info('get_candle_history() - test case 3: ok, correct exception raised!')
                else:
                    raise RuntimeError('test case 3: unexpected exception raised!')
            else:
                raise RuntimeError('test case 3: invalid call did not raise!')

        # test case 4: test call with invalid args type
        if False:
            try:
                yield self.call(procedure, 'foo', 'bar')
            except Exception as e:
                if isinstance(e, ApplicationError) and e.error == 'wamp.error.invalid_argument':
                    if 'invalid type' not in e.args[0]:
                        raise RuntimeError('test case 4: did not find expected error text in exception!')
                    else:
                        self.log.info('get_candle_history() - test case 4: ok, correct exception raised!')
                else:
                    raise RuntimeError('test case 4: unexpected exception raised!')
            else:
                raise RuntimeError('test case 4: invalid call did not raise!')

        # test case 5: test call with invalid kwargs present
        if False:
            try:
                yield self.call(procedure, 12, txaio.time_ns(), foo=23)
            except Exception as e:
                if isinstance(e, ApplicationError) and e.error == 'wamp.error.invalid_argument':
                    if 'unexpected keyword argument' not in e.args[0]:
                        raise RuntimeError('test case 5: did not find expected error text in exception!')
                    else:
                        self.log.info('get_candle_history() - test case 5: ok, correct exception raised!')
                else:
                    raise RuntimeError('test case 5: unexpected exception raised!')
            else:
                raise RuntimeError('test case 5: invalid call did not raise!')

        # test case 6: test call with invalid _result_ key present
        if False:
            try:
                period['period_dur'] = 8
                yield self.call(procedure, period)
            except Exception as e:
                if isinstance(e, ApplicationError) and e.error == 'wamp.error.invalid_argument':
                    if 'invalid type' not in e.args[0]:
                        raise RuntimeError('test case 6: did not find expected error text in exception!')
                    else:
                        self.log.info('get_candle_history() - test case 6: ok, correct exception raised!')
                else:
                    raise RuntimeError('test case 6: unexpected exception raised!')
            else:
                raise RuntimeError('test case 6: invalid call did not raise!')

        # test case 7: test call with invalid _result_ type in (valid) key
        if False:
            try:
                period['period_dur'] = 3
                yield self.call(procedure, period)
            except Exception as e:
                if isinstance(e, ApplicationError) and e.error == 'wamp.error.invalid_argument':
                    if 'invalid type' not in e.args[0]:
                        raise RuntimeError('test case 7: did not find expected error text in exception!')
                    else:
                        self.log.info('get_candle_history() - test case 7: ok, correct exception raised!')
                else:
                    raise RuntimeError('test case 7: unexpected exception raised!')
            else:
                raise RuntimeError('test case 7: invalid call did not raise!')

        self.leave()

    def onLeave(self, details: CloseDetails):
        self.log.info('{func} session closed: {details}', func=hltype(self.onLeave), details=details)
        self.config.extra['exit_details'] = details
        self.disconnect()

    def onDisconnect(self):
        self.log.info('{func} connection to router closed', func=hltype(self.onDisconnect))
        try:
            reactor.stop()
        except ReactorNotRunning:
            pass


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--debug', dest='debug', action='store_true',
                        default=False, help='Enable logging at level "debug".')
    parser.add_argument('--url', dest='url', type=str, default='ws://localhost:8080/ws',
                        help='The router URL (default: ws://localhost:8080/ws).')
    parser.add_argument('--realm', dest='realm', type=str, default=None,
                        help='The realm to join. If not provided, let the router auto-choose the realm.')
    parser.add_argument('--authid', dest='authid', type=str, default=None,
                        help='The authid to connect under. If not provided, let the router auto-choose the authid.')
    parser.add_argument('--key', dest='key', type=str, required=True,
                        help='The private client key to use for authentication. A 32 bytes file containing the raw '
                             'Ed25519 private key.')
    options = parser.parse_args()

    if options.debug:
        txaio.start_logging(level='debug')
    else:
        txaio.start_logging(level='info')

    extra = {
        'authid': options.authid,
        'key': options.key,
        'exit_details': Optional[CloseDetails]
    }
    runner = ApplicationRunner(url=options.url, realm=options.realm, extra=extra)
    runner.run(ExampleClient)

    if isinstance(extra['exit_details'], CloseDetails) and extra['exit_details'].reason == 'wamp.close.normal':
        sys.exit(0)
    else:
        print(extra['exit_details'])
        sys.exit(1)
