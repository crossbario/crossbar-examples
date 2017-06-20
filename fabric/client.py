import txaio
txaio.use_twisted()

from twisted.internet import reactor
from twisted.internet.error import ReactorNotRunning
from autobahn.twisted.wamp import ApplicationSession
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

        # used for user login/registration activation code
        for k in [u'activation_code', u'request_new_activation_code']:
            if k in self.config.extra and self.config.extra[k]:
                extra[k] = self.config.extra[k]

        # now request to join ..
        # now request to join ..
        self.join(self.config.realm,
                  authmethods=[u'cryptosign'],
                  authid=self.config.extra.get(u'authid', None),
                  authrole=self.config.extra.get(u'authrole', None),
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

        # some ApplicationErrors are actually signaling progress
        # in the authentication flow, some are real errors

#        if e.error.startswith(u'fabric.auth-failed.'):
#            error = e.error.split(u'.')[2]
#            message = e.args[0]
#
#            if error == u'new-user-auth-code-sent':
#
#                self.log.info('\nThanks for registering! {}'.format(message))
#                self.log.info(style_ok('Please check your inbox and run "cbsh auth --code <THE CODE YOU GOT BY EMAIL>.\n'))
#
#            elif error == u'registered-user-auth-code-sent':
#
#                self.log.info('\nWelcome back! {}'.format(message))
#                self.log.info(style_ok('Please check your inbox and run "cbsh auth --code <THE CODE YOU GOT BY EMAIL>.\n'))
#
#            elif error == u'pending-activation':
#
#                self.log.info()
#                self.log.info(style_ok(message))
#                self.log.info()
#                self.log.info('Tip: to activate, run "cbsh auth --code <THE CODE YOU GOT BY EMAIL>"')
#                self.log.info('Tip: you can request sending a new code with "cbsh auth --new-code"')
#                self.log.info()
#
#            elif error == u'no-pending-activation':
#
#                exit_code = 1
#                self.log.info()
#                self.log.info(style_error('{} [{}]'.format(message, e.error)))
#                self.log.info()
#
#            elif error == u'email-failure':
#
#                exit_code = 1
#                self.log.info()
#                self.log.info(style_error('{} [{}]'.format(message, e.error)))
#                self.log.info()
#
#            elif error == u'invalid-activation-code':
#
#                exit_code = 1
#                self.log.info()
#                self.log.info(style_error('{} [{}]'.format(message, e.error)))
#                self.log.info()
#
#            else:
#
#                # we should not arrive here! otherwise, add a new clause above and handle the situation
#                exit_code = 1
#                self.log.info(style_error('Internal error: unprocessed error type {}:'.format(error)))
#                self.log.info(style_error(message))
#
#        elif e.error.startswith(u'crossbar.error.'):
#
#            error = e.error.split(u'.')[2]
#            message = e.args[0]
#
#            if error == u'invalid_configuration':
#
#                self.log.info()
#                self.log.info(style_error('{} [{}]'.format(message, e.error)))
#                self.log.info()
#            else:
#
#                # we should not arrive here! otherwise, add a new clause above and handle the situation
#                exit_code = 1
#                self.log.info(style_error('Internal error: unprocessed error type {}:'.format(error)))
#                self.log.info(style_error(message))
#
#        else:
#
#            self.log.info(style_error('{}'.format(e)))
#            exit_code = 1
#            raise

        self.disconnect()

    def onDisconnect(self):
        self.log.info("connection to router closed")
        try:
            reactor.stop()
        except ReactorNotRunning:
            pass


def main():
    import six
    import sys
    import os
    import argparse
    from autobahn.twisted.wamp import ApplicationRunner

    # parse command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--debug', dest='debug', action='store_true', default=False, help='Enable logging at level "debug".')
    parser.add_argument('--authid', dest='authid', type=six.text_type, default=None, help='The authid to connect under. If not provided, let the router auto-choose the authid.')
    parser.add_argument('--activation_code', dest='activation_code', type=six.text_type, default=None, help='An activation code when still pairing the authentication key pair with CDC.')
    parser.add_argument('--realm', dest='realm', type=six.text_type, default=None, help='The realm to join. If not provided, let the router auto-choose the realm.')
    parser.add_argument('--key', dest='key', type=six.text_type, default=u'priv.key', help='The private client key file to use for authentication. A 32 bytes file containing the raw Ed25519 private key.')
    parser.add_argument('--routerkey', dest='routerkey', type=six.text_type, default=None, help='The public router key to verify the remote router against. A 32 bytes file containing the raw Ed25519 public key.')
    parser.add_argument('--url', dest='url', type=six.text_type, default=u'ws://localhost:9000/ws', help='The router URL (default: ws://localhost:8080/ws).')
    parser.add_argument('--agent', dest='agent', type=six.text_type, default=None, help='Path to Unix domain socket of SSH agent to use.')
    options = parser.parse_args()

    # authid=
    # authextra=6R3T-NXH9-WS7K

    if options.debug:
        txaio.start_logging(level='debug')
    else:
        txaio.start_logging(level='info')

    if not os.path.exists(options.key):
        with open(options.key, 'wb') as f:
            # generate new key: simply, 32 bytes cryptographically strong random noise
            data = os.urandom(32)
            f.write(data)
        print("New key generated and key file written!")
    else:
        print("Loading key from existing key file.")

    # forward infos to ClientSession
    extra = {
        u'authid': options.authid,
        u'key': options.key,
        u'activation_code': options.activation_code,
        u'request_new_activation_code': False
    }
    print("Connecting to {}: realm={}, authid={}".format(options.url, options.realm, options.authid))

    # connect to router and run ClientSession
    runner = ApplicationRunner(url=options.url, realm=options.realm, extra=extra)
    runner.run(ClientSession)


if __name__ == '__main__':
    main()
