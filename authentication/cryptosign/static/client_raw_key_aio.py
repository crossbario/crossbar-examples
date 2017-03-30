from os import environ

try:
    import asyncio
except ImportError:
    import trollius as asyncio

from autobahn.asyncio.wamp import ApplicationSession, ApplicationRunner
from autobahn.wamp import cryptosign


class ClientSession(ApplicationSession):

    def __init__(self, config=None):
        self.log.info("initializing component: {config}", config=config)
        ApplicationSession.__init__(self, config)

        # load the client private key (raw format)
        try:
            self._key = cryptosign.SigningKey.from_raw_key(config.extra[u'key'])
        except Exception as e:
            self.log.error("could not load client private key: {log_failure}", log_failure=e)
            self.leave()
        else:
            self.log.info("client public key loaded: {}".format(self._key.public_key()))

    def onConnect(self):
        self.log.info("connected to router")

        # authentication extra information for wamp-cryptosign
        #
        extra = {
            # forward the client pubkey: this allows us to omit authid as
            # the router can identify us with the pubkey already
            u'pubkey': self._key.public_key(),

            # not yet implemented. a public key the router should provide
            # a trustchain for it's public key. the trustroot can eg be
            # hard-coded in the client, or come from a command line option.
            u'trustroot': None,

            # not yet implemented. for authenticating the router, this
            # challenge will need to be signed by the router and send back
            # in AUTHENTICATE for client to verify. A string with a hex
            # encoded 32 bytes random value.
            u'challenge': None,

            u'channel_binding': u'tls-unique'
        }

        # now request to join ..
        self.join(self.config.realm,
                  authmethods=[u'cryptosign'],
                  authid=self.config.extra[u'authid'],
                  authextra=extra)

    def onChallenge(self, challenge):
        self.log.info("authentication challenge received: {challenge}", challenge=challenge)
        # alright, we've got a challenge from the router.

        # not yet implemented. check the trustchain the router provided against
        # our trustroot, and check the signature provided by the
        # router for our previous challenge. if both are ok, everything
        # is fine - the router is authentic wrt our trustroot.

        # sign the challenge with our private key.
        signed_challenge = self._key.sign_challenge(self, challenge)

        # send back the signed challenge for verification
        return signed_challenge

    def onJoin(self, details):
        self.log.info("session joined: {details}", details=details)
        self.log.info("*** Hooray! We've been successfully authenticated with WAMP-cryptosign using Ed25519! ***")
        self.leave()

    def onLeave(self, details):
        self.log.info("session closed: {details}", details=details)
        self.disconnect()

    def onDisconnect(self):
        self.log.info("connection to router closed")
        loop = asyncio.get_event_loop()
        loop.stop()


if __name__ == '__main__':

    import six
    import sys
    import argparse

    # parse command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--debug', dest='debug', action='store_true', default=False, help='Enable logging at level "debug".')
    parser.add_argument('--authid', dest='authid', type=six.text_type, default=None, help='The authid to connect under. If not provided, let the router auto-choose the authid.')
    parser.add_argument('--realm', dest='realm', type=six.text_type, default=None, help='The realm to join. If not provided, let the router auto-choose the realm.')
    parser.add_argument('--key', dest='key', type=six.text_type, required=True, help='The private client key to use for authentication. A 32 bytes file containing the raw Ed25519 private key.')
    parser.add_argument('--routerkey', dest='routerkey', type=six.text_type, default=None, help='The public router key to verify the remote router against. A 32 bytes file containing the raw Ed25519 public key.')
    parser.add_argument('--url', dest='url', type=six.text_type, default=u'ws://localhost:8080/ws', help='The router URL (default: ws://localhost:8080/ws).')
    parser.add_argument('--agent', dest='agent', type=six.text_type, default=None, help='Path to Unix domain socket of SSH agent to use.')
    options = parser.parse_args()

    # forward requested authid and key filename to ClientSession
    extra = {
        u'authid': options.authid,
        u'key': options.key
    }
    print("Connecting to {}: realm={}, authid={}".format(options.url, options.realm, options.authid))

    # connect to router and run ClientSession
    runner = ApplicationRunner(url=options.url, realm=options.realm, extra=extra)
    runner.run(ClientSession)
