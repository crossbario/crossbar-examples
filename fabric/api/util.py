import os

import txaio
txaio.use_twisted()

from twisted.internet import reactor
from twisted.internet.error import ReactorNotRunning
from twisted.internet.defer import inlineCallbacks

from autobahn.wamp import cryptosign
from autobahn.twisted.wamp import ApplicationSession, ApplicationRunner


class CDCClient(ApplicationSession):

    def onConnect(self):
        self.log.debug('CDC connection established - joining realm ..')

        # authentication extra information for wamp-cryptosign
        #
        extra = {
            # forward the client pubkey: this allows us to omit authid as
            # the router can identify us with the pubkey already
            u'pubkey': self.config.extra[u'key'].public_key(),

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
                  authextra=extra)

    def onChallenge(self, challenge):
        self.log.debug("CDC authentication challenge received: {challenge}", challenge=challenge)
        # alright, we've got a challenge from the router.

        # not yet implemented. check the trustchain the router provided against
        # our trustroot, and check the signature provided by the
        # router for our previous challenge. if both are ok, everything
        # is fine - the router is authentic wrt our trustroot.

        # sign the challenge with our private key.
        signed_challenge = self.config.extra[u'key'].sign_challenge(self, challenge)

        # send back the signed challenge for verification
        return signed_challenge

    @inlineCallbacks
    def onJoin(self, details):
        self.log.debug("CDC session ready: {details}", details=details)
        yield self.config.extra[u'on_ready'](self)
        self.leave()

    def onLeave(self, details):
        self.log.debug("CDC session closed: {details}", details=details)
        self.disconnect()

    def onDisconnect(self):
        self.log.debug("CDC connection closed.")
        try:
            reactor.stop()
        except ReactorNotRunning:
            pass


def run(on_ready, keyfile='mykey'):
    if not keyfile:
        keyfile = os.path.join(os.path.expanduser('~'), '.ssh', 'id_ed25519')

    key = cryptosign.SigningKey.from_ssh_key(keyfile)

    extra = {
        u'key': key,
        u'on_ready': on_ready
    }

    runner = ApplicationRunner(
        u'ws://127.0.0.1:8080/ws',
        None,
        extra=extra,
    )

    runner.run(CDCClient)
