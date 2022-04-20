import os
import sys
from pprint import pformat, pprint
import werkzeug

from twisted.internet import reactor
from twisted.internet.defer import inlineCallbacks

from autobahn.twisted.wamp import ApplicationSession
from autobahn.wamp import auth
from autobahn.util import hltype


class ClientSession(ApplicationSession):

    def __init__(self, config):
        super().__init__(config)
        self.log.info('{meth}(config=\n{config}): init completed',
                      meth=hltype(self.__init__),
                      config=config)

    def onConnect(self):
        self.log.info('{meth}()', meth=hltype(self.onConnect))

        # autobahn.twisted.websocket.WampWebSocketClientProtocol
        pprint(self.transport.http_headers)
        pprint(self.transport.transport_details.marshal())

        if self.config.extra['cookie']:
            authmethods = ['cookie']
        else:
            authmethods = ['wampcra']

        self.log.info('{meth}: joining realm "{realm}" as "{authid}" using authmethods {authmethods}',
                      meth=hltype(self.onConnect),
                      realm=self.config.realm,
                      authid=self.config.extra.get('authid', None),
                      authmethods=authmethods)
        self.join(self.config.realm, authmethods, self.config.extra.get('authid', None))

    def onChallenge(self, challenge):
        self.log.info('{meth}(challenge=\n{challenge})', meth=hltype(self.onChallenge),
                      challenge=challenge)

        if challenge.method == 'wampcra':
            if 'salt' in challenge.extra:
                # salted secret
                key = auth.derive_key(self.config.extra['secret'],
                                      challenge.extra['salt'],
                                      challenge.extra['iterations'],
                                      challenge.extra['keylen'])
            else:
                # plain, unsalted secret
                key = self.config.extra['secret']

            signature = auth.compute_wcs(key, challenge.extra['challenge'])

            return signature
        else:
            raise Exception('Challenge received for unexpected authmethod "{}"'.format(challenge.method))

    @inlineCallbacks
    def onJoin(self, details):
        self.log.info('{meth}(details=\n{details})', meth=hltype(self.onJoin),
                      details=details)

        # 'set-cookie': 'cbtid=pNXWaQASsPqjhHoWEInL3Hzv;max-age=604800'
        if hasattr(self.transport, 'http_headers') and 'set-cookie' in self.transport.http_headers:
            cookie_name = 'cbtid'
            cookie_received = self.transport.http_headers['set-cookie']
            cookie_sent = str(
                werkzeug.http.dump_cookie(cookie_name, werkzeug.http.parse_cookie(cookie_received)[cookie_name],
                                          path=None))
            self.config.extra['cookie'] = cookie_sent
            self.transport.factory.headers['Set-Cookie'] = cookie_sent

        res = yield self.call('com.example.add2', 23, 666)
        assert res == 689
        self.log.info('\n\nRPC result (success): {res}\n\n', res=res)

        self.config.extra['run_log'].append(
            [self.config.extra['run_count'], details.realm, details.authid, details.authrole, details.authmethod,
             details.authprovider])

        self.leave()

    def onLeave(self, details):
        self.log.info('{meth}(details={details})', meth=hltype(self.onLeave),
                      details=details)

        self.config.extra['exit_details'] = details

        if details.reason == 'wamp.close.normal':
            pass
        elif details.reason == 'wamp.error.not_authorized':
            self.config.extra['cookie'] = None
        else:
            pass

        self.disconnect()

    def onDisconnect(self):
        self.log.info('{meth}()', meth=hltype(self.onDisconnect))
        if self.config.extra['run_count']:
            self.config.extra['run_count'] -= 1
        else:
            self.config.extra['runner'].stop()
            reactor.stop()


if __name__ == '__main__':

    if 'MYSECRET' in os.environ and len(sys.argv) > 1:
        # principal from command line, secret from environment variable
        USER = sys.argv[1]
        USER_SECRET = os.environ['MYSECRET']
    else:
        raise RuntimeError('missing authid or auth secret (from env var MYSECRET)')

    from autobahn.twisted.wamp import ApplicationRunner

    extra = {
        'authid': USER,
        'secret': USER_SECRET,
        'exit_details': None,
        'cookie': None,
        'run_count': 3,
        'run_log': [],
    }

    runner = ApplicationRunner(url='ws://localhost:8080/ws', realm='realm1', extra=extra)
    extra['runner'] = runner

    runner.run(ClientSession, auto_reconnect=True)

    pprint(extra['run_log'])

    if not extra['exit_details'] or extra['exit_details'].reason != 'wamp.close.normal':
        print('FAILED')
        sys.exit(1)
    else:
        print('SUCCESS')
        sys.exit(0)
