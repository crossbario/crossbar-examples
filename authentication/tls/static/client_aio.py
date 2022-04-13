from autobahn.wamp import cryptosign
from autobahn.asyncio.wamp import ApplicationSession, ApplicationRunner
import asyncio
import txaio
txaio.use_asyncio()


class ClientSession(ApplicationSession):

    # when running over TLS, require TLS channel binding
    CHANNEL_BINDING = 'tls-unique'
    # CHANNEL_BINDING = None

    def __init__(self, config=None):
        self.log.info("initializing component: {config}", config=config)
        ApplicationSession.__init__(self, config)

        # load the client private key (raw format)
        try:
            self._key = cryptosign.SigningKey.from_raw_key(config.extra['key'])
        except Exception as e:
            self.log.error(
                "could not load client private key: {log_failure}", log_failure=e)
            self.leave()
        else:
            self.log.info("client public key loaded: {}".format(
                self._key.public_key()))

        # when running over TLS, require TLS channel binding: None or "tls-unique"
        self._req_channel_binding = config.extra['channel_binding']

    def onConnect(self):
        self.log.info("connected to router")

        # authentication extra information for wamp-cryptosign
        #
        extra = {
            # forward the client pubkey: required!
            'pubkey': self._key.public_key(),

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
                  authmethods=['cryptosign'],
                  # authid may bee None for WAMP-cryptosign!
                  authid=self.config.extra['authid'],
                  authextra=extra)

    def onChallenge(self, challenge):
        self.log.info(
            "authentication challenge received: {challenge}", challenge=challenge)
        # alright, we've got a challenge from the router.

        # not yet implemented. check the trustchain the router provided against
        # our trustroot, and check the signature provided by the
        # router for our previous challenge. if both are ok, everything
        # is fine - the router is authentic wrt our trustroot.

        assert challenge.method == 'cryptosign'
        assert challenge.extra['channel_binding'] == self._req_channel_binding

        # sign the challenge with our private key.
        signed_challenge = self._key.sign_challenge(
            self, challenge, channel_id_type=ClientSession.CHANNEL_BINDING)

        print(challenge)
        print(signed_challenge)

        # send back the signed challenge for verification
        return signed_challenge

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
        loop = asyncio.get_event_loop()
        loop.stop()


if __name__ == '__main__':

    import sys
    import argparse

    # parse command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--debug', dest='debug', action='store_true',
                        default=False, help='Enable logging at level "debug".')
    parser.add_argument('--channel_binding', dest='channel_binding', type=str, default=None,
                        help='TLS channel binding: None or "tls-unique"')
    parser.add_argument('--authid', dest='authid', type=str, default=None,
                        help='The authid to connect under. If not provided, let the router auto-choose the authid.')
    parser.add_argument('--realm', dest='realm', type=str, default=None,
                        help='The realm to join. If not provided, let the router auto-choose the realm.')
    parser.add_argument('--key', dest='key', type=str, required=True,
                        help='The private client key to use for authentication. A 32 bytes file containing the raw Ed25519 private key.')
    parser.add_argument('--routerkey', dest='routerkey', type=str, default=None,
                        help='The public router key to verify the remote router against. A 32 bytes file containing the raw Ed25519 public key.')
    parser.add_argument('--url', dest='url', type=str, default='ws://localhost:8080/ws',
                        help='The router URL (default: ws://localhost:8080/ws).')
    parser.add_argument('--agent', dest='agent', type=str, default=None,
                        help='Path to Unix domain socket of SSH agent to use.')
    options = parser.parse_args()

    # forward requested authid and key filename to ClientSession
    extra = {
        'channel_binding': options.channel_binding,

        # this is optional
        'authid': options.authid,

        # the private key is required
        'key': options.key,

        'exit_details': None,
    }
    print("Connecting to {}: requesting realm={}, authid={}".format(
        options.url, options.realm, options.authid))

    tls_config = {
        "hostname": "localhost",
        # "certificate": "client.crt",
        # "key": "client.key",
        "ca_certificates": [
            "intermediate.cert.pem",
            "ca.cert.pem"
        ]
    }

    # FIXME: forward TLS certification options ^ to ApplicationRunner

    # connect to router and run ClientSession
    runner = ApplicationRunner(
        url=options.url, realm=options.realm, extra=extra)
    runner.run(ClientSession)

    # CloseDetails(reason=<wamp.error.not_authorized>, message='WAMP-CRA signature is invalid')
    print(extra['exit_details'])

    if extra['exit_details'].reason != 'wamp.close.normal':
        sys.exit(1)
    else:
        sys.exit(0)
