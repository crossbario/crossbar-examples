import os
import binascii
from binascii import b2a_hex
from pprint import pformat

import nacl
from nacl.exceptions import BadSignatureError
from nacl.signing import VerifyKey

from twisted.internet.defer import inlineCallbacks
from twisted.internet.error import ReactorNotRunning
from twisted.internet import reactor

import txaio
txaio.use_twisted()
from txaio import make_logger

from autobahn.util import hltype
from autobahn.wamp import cryptosign
from autobahn.twisted.wamp import ApplicationSession
from crossbar.common.twisted.endpoint import _create_tls_client_context

from autobahn.wamp.cryptosign import CryptosignKey
from autobahn.xbr import make_w3, EthereumKey
from autobahn.xbr._secmod import SecurityModuleMemory
from autobahn.xbr import create_eip712_delegate_certificate, create_eip712_authority_certificate


class ClientSession(ApplicationSession):

    def __init__(self, config=None):
        self.log.info('{func} initializing component: {config}', func=hltype(self.__init__), config=config)
        ApplicationSession.__init__(self, config)

        self._key = None
        self._eth_key = None
        if False:
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
        else:
            self._sm: SecurityModuleMemory = SecurityModuleMemory.from_seedphrase(self.config.extra['seedphrase'], num_eth_keys=5, num_cs_keys=5)

        self._gw_config = {
            'type': 'infura',
            'key': os.environ.get('WEB3_INFURA_PROJECT_ID', ''),
            'network': 'mainnet',
        }
        self._w3 = make_w3(self._gw_config)

    @inlineCallbacks
    def onConnect(self):
        self.log.info('{func} connected to router', func=hltype(self.onConnect))

        assert self._w3.isConnected()

        yield self._sm.open()

        self._eth_key: EthereumKey = self._sm[1]
        self._key: CryptosignKey = self._sm[6]

        chainId = self._w3.eth.chain_id
        verifyingContract = binascii.a2b_hex('0xf766Dc789CF04CD18aE75af2c5fAf2DA6650Ff57'[2:])
        validFrom = self._w3.eth.block_number
        delegate = self._eth_key.address(binary=True)
        csPubKey = self._key.public_key(binary=True)
        bootedAt = txaio.time_ns()

        cert_data = create_eip712_delegate_certificate(chainId=chainId, verifyingContract=verifyingContract,
                                                       validFrom=validFrom, delegate=delegate, csPubKey=csPubKey,
                                                       bootedAt=bootedAt)

        # print('\n\n{}\n\n'.format(pformat(cert_data)))

        cert_sig = yield self._eth_key.sign_typed_data(cert_data, binary=False)

        cert_data['message']['csPubKey'] = b2a_hex(cert_data['message']['csPubKey']).decode()
        cert_data['message']['delegate'] = self._w3.toChecksumAddress(cert_data['message']['delegate'])
        cert_data['message']['verifyingContract'] = self._w3.toChecksumAddress(cert_data['message']['verifyingContract'])

        # authentication extra information for wamp-cryptosign
        authextra = {
            # forward the client pubkey: required!
            'pubkey': self._key.public_key(),

            # when running over TLS, require TLS channel binding
            'channel_binding': self.config.extra['channel_binding'],

            # not yet implemented. a public key the router should provide
            # a trust chain for its public key. the trustroot can e.g. be
            # hard-coded in the client, or come from a command line option.
            'trustroot': self.config.extra['trustroot'],

            # certificate chain beginning with delegate certificate for this client (the delegate)
            'certificates': [(cert_data, cert_sig)],

            # for authenticating the router, this challenge will need to be signed by
            # the router and send back in AUTHENTICATE for client to verify.
            # A string with a hex encoded 32 bytes random value.
            'challenge': self.config.extra['challenge'],
        }
        self.log.info('authenticating using authextra:\n\n{authextra}\n', authextra=pformat(authextra))

        # now request to join
        self.join(self.config.realm,
                  authmethods=['cryptosign'],
                  # authid may bee None for WAMP-cryptosign!
                  authid=self.config.extra.get('authid', None),
                  authextra=authextra)

    def onChallenge(self, challenge):
        self.log.info('{func} authentication challenge received: {challenge}',
                      func=hltype(self.onChallenge), challenge=challenge)

        # check the trustchain the router provided against
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

        channel_id = self.transport.transport_details.channel_id.get(self.config.extra['channel_binding'], None)

        # sign the challenge with our private key.
        signed_challenge = self._key.sign_challenge(challenge,
                                                    channel_id=channel_id,
                                                    channel_id_type=self.config.extra['channel_binding'])

        # send back the signed challenge for verification
        return signed_challenge

    def onJoin(self, details):
        self.log.info('{func} session joined: {details}', func=hltype(self.onJoin), details=details)
        self.log.info('*' * 80)
        self.log.info('OK, successfully authenticated with WAMP-cryptosign: realm="{realm}", authid="{authid}", authrole="{authrole}"',
                      realm=details.realm, authid=details.authid, authrole=details.authrole)
        self.log.info('*' * 80)
        self.leave()


    @inlineCallbacks
    def onLeave(self, details):
        self.log.info("{func} session closed: {details}", func=hltype(self.onLeave), details=details)
        self.config.extra['exit_details'] = details

        yield self._sm.close()

        self.disconnect()

    def onDisconnect(self):
        self.log.info('{func} connection to router closed', func=hltype(self.onDisconnect))
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
                        help='Optional TLS channel binding, e.g. "tls-unique"')
    parser.add_argument('--trustroot', dest='trustroot', type=str, default=None,
                        help='Optional client trustroot, e.g. "0xf766Dc789CF04CD18aE75af2c5fAf2DA6650Ff57"')
    parser.add_argument('--challenge', dest='challenge', action='store_true',
                        default=False, help='Enable router challenge.')
    parser.add_argument('--authid', dest='authid', type=str, default=None,
                        help='The authid to connect under. If not provided, let the router auto-choose the authid.')
    parser.add_argument('--realm', dest='realm', type=str, default='devices',
                        help='The realm to join. If not provided, let the router auto-choose the realm.')
    parser.add_argument('--key', dest='key', type=str, required=True,
                        help='The WAMP-Cryptosign private client key to use for authentication. A 32 bytes file containing the raw Ed25519 private key.')
    parser.add_argument('--url', dest='url', type=str, default='wss://localhost:8080/ws',
                        help='The router URL (default: wss://localhost:8080/ws).')
    options = parser.parse_args()

    if options.debug:
        # txaio.start_logging(level='debug')
        txaio.start_logging(level='trace')
    else:
        txaio.start_logging(level='info')
    log = make_logger()

    # forward requested authid and key filename to ClientSession
    extra = {
        'channel_binding': options.channel_binding,
        'trustroot': options.trustroot,
        'challenge': binascii.b2a_hex(os.urandom(32)).decode() if options.challenge else None,
        'authid': options.authid,

        # 'key': options.key,
        'seedphrase': "avocado style uncover thrive same grace crunch want essay reduce current edge",

        'exit_details': None,
    }
    print("Connecting to {}: requesting realm={}, authid={}".format(
        options.url, options.realm, options.authid))

    tls_config = {
        "hostname": "localhost",
        "ca_certificates": [
            "intermediate.cert.pem",
            "ca.cert.pem"
        ],

        # TLS client key and certificate
        # "key": "client.key",
        # "certificate": "client.crt",
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
