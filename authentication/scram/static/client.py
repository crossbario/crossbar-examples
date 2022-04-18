import os
import sys
import base64
import argparse
from pprint import pprint
import werkzeug

import txaio
txaio.use_twisted()

from twisted.internet import reactor
from twisted.internet.defer import inlineCallbacks

from autobahn.twisted.wamp import ApplicationSession, ApplicationRunner
from autobahn.wamp import auth
from autobahn.xbr._util import hltype


class ClientSession(ApplicationSession):

    def __init__(self, config):
        super().__init__(config)
        self.log.info('{meth}(config=\n{config}): init completed',
                      meth=hltype(self.__init__),
                      config=config)

    def onConnect(self):
        self.log.info('{meth}()', meth=hltype(self.onConnect))
        try:
            realm = self.config.realm
            authid = self.config.extra.get('authid', None)
            password = self.config.extra.get('password', None)

            self._scram_auth = auth.AuthScram(
                nonce=base64.b64encode(os.urandom(16)).decode('ascii'),
                kdf='argon2id13',
                salt='salt123',
                iterations=4096,
                memory=512,
                password=password,
                authid=authid,
            )

            authmethods = ['scram']
            authextra = self._scram_auth.authextra

            self.log.info('{meth}: joining realm "{realm}" as "{authid}" using authmethods {authmethods}',
                          meth=hltype(self.onConnect),
                          realm=realm,
                          authid=authid,
                          authmethods=authmethods,
                          authextra=authextra)
            self.join(realm, authmethods, authid, authextra=authextra)
        except:
            self.log.failure()

    def onChallenge(self, challenge):
        self.log.info('{meth}(challenge=\n{challenge})', meth=hltype(self.onChallenge),
                      challenge=challenge)

        if challenge.method == 'scram':
            signature = self._scram_auth.on_challenge(self, challenge)
            return signature
        else:
            raise Exception('Challenge received for unexpected authmethod "{}"'.format(challenge.method))

    def onJoin(self, details):
        self.log.info('{meth}(details=\n{details})', meth=hltype(self.onJoin),
                      details=details)

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

    parser = argparse.ArgumentParser()
    parser.add_argument('--debug', dest='debug', action='store_true',
                        default=False, help='Enable logging at level "debug".')
    parser.add_argument('--url', dest='url', type=str, default='ws://localhost:8080/ws',
                        help='The router URL (default: ws://localhost:8080/ws).')
    parser.add_argument('--realm', dest='realm', type=str, default="realm1",
                        help='The realm to join. If not provided, let the router auto-choose the realm.')
    parser.add_argument('--authid', dest='authid', type=str, default="foobar@example.com",
                        help='The authid to connect under. If not provided, let the router auto-choose the authid.')
    parser.add_argument('--password', dest='password', type=str,
                        help='The password to use.')
    options = parser.parse_args()

    if options.debug:
        txaio.start_logging(level='debug')
    else:
        txaio.start_logging(level='info')

    extra = {
        'authid': options.authid,
        'password': options.password,
        'exit_details': None,
        'run_count': 1,
        'run_log': [],
    }

    runner = ApplicationRunner(url='ws://localhost:8080/ws', realm=options.realm, extra=extra)
    extra['runner'] = runner

    runner.run(ClientSession, auto_reconnect=True)

    pprint(extra['run_log'])

    if not extra['exit_details'] or extra['exit_details'].reason != 'wamp.close.normal':
        print('FAILED')
        sys.exit(1)
    else:
        print('SUCCESS')
        sys.exit(0)
