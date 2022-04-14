import os
import sys
from pprint import pformat, pprint

from twisted.internet import reactor
from twisted.internet.defer import inlineCallbacks

from autobahn.twisted.wamp import ApplicationSession
from autobahn.wamp import auth
from autobahn.xbr._util import hltype


class ClientSession(ApplicationSession):

    def __init__(self, config):
        super().__init__(config)
        self._authmethods_next = None

    def onConnecting(self, transport_details, connecting_request):
        self.log.debug('{meth}(transport_details=\n{transport_details},\nconnecting_request=\n{connecting_request})',
                       meth=hltype(self.onConnecting),
                       transport_details=pformat(transport_details.__json__()),
                       connecting_request=pformat(connecting_request.__json__()))

        # check if we have stored a cookie from a previous successful authentication
        cookie = self.config.extra.get('cookie', None)
        if cookie:
            connecting_request.headers['Cookie'] = cookie
            self._authmethods_next = ['cookie']
        else:
            # self._authmethods_next = ['wampcra', 'cookie']
            self._authmethods_next = ['wampcra']

        connecting_request.useragent = 'SilverSurfer2022'

        self.log.debug('{meth}: connecting with connecting_request=\n{connecting_request}',
                       meth=hltype(self.onConnecting),
                       connecting_request=pformat(connecting_request.__json__()))
        return connecting_request

    def onConnect(self, connection_response):
        self.log.debug('{meth}(connection_response=\n{connection_response})', meth=hltype(self.onConnect),
                       connection_response=pformat(connection_response.__json__()) if connection_response else None)

        # 'set-cookie': 'cbtid=pNXWaQASsPqjhHoWEInL3Hzv;max-age=604800'
        if 'set-cookie' in connection_response.headers:
            self.config.extra['cookie'] = connection_response.headers['set-cookie']

        self.log.info('{meth}: joining realm "{realm}" as "{authid}" using authmethods {authmethods}',
                      meth=hltype(self.onConnect),
                      realm=self.config.realm,
                      authid=self.config.extra.get('authid', None),
                      authmethods=self._authmethods_next)
        self.join(self.config.realm, self._authmethods_next, self.config.extra.get('authid', None))

    def onChallenge(self, challenge):
        self.log.debug('{meth}(challenge=\n{challenge})', meth=hltype(self.onChallenge),
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
        'run_count': 2,
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
