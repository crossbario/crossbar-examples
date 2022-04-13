import sys
import os
from binascii import b2a_hex, a2b_hex
from autobahn.wamp import cryptosign
from autobahn.twisted.wamp import ApplicationSession
from twisted.internet.error import ReactorNotRunning
from twisted.internet import reactor
from crossbar.common.twisted.endpoint import _create_tls_client_context

import txaio
txaio.use_twisted()

from txaio import make_logger


class ClientSession(ApplicationSession):

    def __init__(self, config=None):
        self.log.info("initializing component: {config}", config=config)
        ApplicationSession.__init__(self, config)

        # when running over TLS, require TLS channel binding: None or "tls-unique"
        self._req_channel_binding = config.extra['channel_binding']

    def onConnect(self):
        self.log.info("connected to router")

        # authentication extra information for wamp-cryptosign
        #
        authextra = {
            # when running over TLS, require TLS channel binding
            'channel_binding': self._req_channel_binding,

            # not yet implemented. a public key the router should provide
            # a trustchain for it's public key. the trustroot can eg be
            # hard-coded in the client, or come from a command line option.
            # 'trustroot': None,

            # not yet implemented. for authenticating the router, this
            # challenge will need to be signed by the router and send back
            # in AUTHENTICATE for client to verify. A string with a hex
            # encoded 32 bytes random value.
            # 'challenge': None,
        }
        self.log.info('authenticating using authextra={authextra} and channel_binding={channel_binding} ..', authextra=extra, channel_binding=self._req_channel_binding)

        # now request to join ..
        self.join(self.config.realm,
                  authmethods=['tls'],
                  authid=self.config.extra.get('authid', None),
                  authextra=authextra)

    def onJoin(self, details):
        self.log.info('session joined: {details}', details=details)
        self.log.info('*' * 80)
        self.log.info('OK, successfully authenticated with WAMP-cryptosign: realm="{realm}", authid="{authid}", authrole="{authrole}"',
                      realm=details.realm, authid=details.authid, authrole=details.authrole)
        self.log.info('*' * 80)
        self.leave()

    def onLeave(self, details):
        self.log.info("session closed: {details}", details=details)
        self.config.extra['exit_details'] = details
        self.disconnect()

    def onDisconnect(self):
        self.log.info("connection to router closed")
        try:
            reactor.stop()
        except ReactorNotRunning:
            pass


if __name__ == '__main__':

    import sys
    import argparse
    from autobahn.twisted.wamp import ApplicationRunner

    # parse command line arguments
    parser = argparse.ArgumentParser()

    parser.add_argument('--debug', dest='debug', action='store_true',
                        default=False, help='Enable logging at level "debug".')
    parser.add_argument('--channel_binding', dest='channel_binding', type=str, default=None,
                        help='TLS channel binding: None or "tls-unique"')
    parser.add_argument('--key', dest='key', type=str, help='The TLS private client key.', default='client.key')
    parser.add_argument('--cert', dest='cert', type=str, help='The TLS client certification .', default='client.crt')
    parser.add_argument('--authid', dest='authid', type=str, default=None,
                        help='The authid to connect under. If not provided, let the router auto-choose the authid.')
    parser.add_argument('--realm', dest='realm', type=str, default='realm1',
                        help='The realm to join. If not provided, let the router auto-choose the realm.')
    parser.add_argument('--url', dest='url', type=str, default='wss://localhost:8080/ws',
                        help='The router URL (default: wss://localhost:8080/ws).')
    options = parser.parse_args()

    if options.debug:
        txaio.start_logging(level='debug')
    else:
        txaio.start_logging(level='info')
    log = make_logger()

    # forward requested authid and key filename to ClientSession
    extra = {
        'channel_binding': options.channel_binding,

        # this is optional
        'authid': options.authid,

        'exit_details': None,
    }
    print("Connecting to {}: requesting realm={}, authid={}".format(
        options.url, options.realm, options.authid))

    tls_config = {
        "hostname": "localhost",
        "certificate": options.cert,
        "key": options.key,
        "ca_certificates": [
            "intermediate.cert.pem",
            "ca.cert.pem"
        ]
    }
    cbdir = os.path.join(os.path.dirname(__file__), '.crossbar')
    cert_options = _create_tls_client_context(tls_config, cbdir, log)

    # connect to router and run ClientSession
    runner = ApplicationRunner(
        url=options.url, realm=options.realm, extra=extra, ssl=cert_options)
    runner.run(ClientSession)

    # CloseDetails(reason=<wamp.error.not_authorized>, message='WAMP-CRA signature is invalid')
    print(extra['exit_details'])

    if extra['exit_details'].reason != 'wamp.close.normal':
        sys.exit(1)
    else:
        sys.exit(0)
