import os
import binascii

import txaio
txaio.use_twisted()

import nacl
from nacl.exceptions import BadSignatureError
from nacl.signing import VerifyKey

from autobahn.util import hltype
from autobahn.wamp import cryptosign
from autobahn.twisted.wamp import ApplicationSession
from twisted.internet.error import ReactorNotRunning
from twisted.internet import reactor


class ClientSession(ApplicationSession):

    # when running over TLS, require TLS channel binding
    # CHANNEL_BINDING = 'tls-unique'
    CHANNEL_BINDING = None

    def __init__(self, config=None):
        self.log.info("initializing component: {config}", config=config)
        ApplicationSession.__init__(self, config)

        # load the client private key (raw format)
        try:
            self._key = cryptosign.CryptosignKey.from_file(config.extra['key'])
        except Exception as e:
            self.log.error(
                "could not load client private key: {log_failure}", log_failure=e)
            self.leave()
        else:
            self.log.info("client public key loaded: {}".format(
                self._key.public_key()))

    def onConnect(self):
        self.log.info("connected to router")

        # authentication extra information for wamp-cryptosign
        #
        extra = {
            # forward the client pubkey: required!
            'pubkey': self._key.public_key(),

            # when running over TLS, require TLS channel binding
            'channel_binding': ClientSession.CHANNEL_BINDING,

            # not yet implemented. a public key the router should provide
            # a trustchain for it's public key. the trustroot can eg be
            # hard-coded in the client, or come from a command line option.
            # 'trustroot': None,

            # for authenticating the router, this challenge will need to be signed by
            # the router and send back in AUTHENTICATE for client to verify.
            # A string with a hex encoded 32 bytes random value.
            'challenge': binascii.b2a_hex(os.urandom(32)).decode(),
        }

        # now request to join
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
        verify_key = None
        if 'pubkey' in challenge.extra:
            verify_key = VerifyKey(challenge.extra['pubkey'], encoder=nacl.encoding.HexEncoder)

        if 'signature' in challenge.extra:
            assert verify_key

            signature = binascii.a2b_hex(challenge.extra['signature'])
            # assert len(signature) == 96, 'unexpected length {} of signature'.format(len(signature))
            try:
                message = verify_key.verify(signature)
            except BadSignatureError:
                raise RuntimeError('invalid router signature for client challenge')
            else:
                self.log.info('{func} ok, successfully verified router signature for router public key {pubkey}',
                              func=hltype(self.onChallenge),
                              pubkey=challenge.extra['pubkey'])

        # sign the challenge with our private key.
        signed_challenge = self._key.sign_challenge(challenge,
                                                    channel_id=self.transport.transport_details.channel_id.get(ClientSession.CHANNEL_BINDING, None),
                                                    channel_id_type=ClientSession.CHANNEL_BINDING)

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

    if options.debug:
        txaio.start_logging(level='debug')
    else:
        txaio.start_logging(level='info')

    # forward requested authid and key filename to ClientSession
    extra = {
        # this is optional
        'authid': options.authid,

        # the private key is required
        'key': options.key,

        'exit_details': None,
    }
    print("Connecting to {}: requesting realm={}, authid={}".format(
        options.url, options.realm, options.authid))

    # connect to router and run ClientSession
    runner = ApplicationRunner(
        url=options.url, realm=options.realm, extra=extra)
    runner.run(ClientSession)

    # CloseDetails(reason=<wamp.error.not_authorized>, message='WAMP-CRA signature is invalid')
    print(extra['exit_details'])

    if not extra['exit_details'] or (extra['exit_details'] and extra['exit_details'].reason != 'wamp.close.normal'):
        sys.exit(1)
    else:
        sys.exit(0)
