import sys
import argparse
from pprint import pprint
from autobahn.twisted.wamp import ApplicationRunner

import os
import binascii
from binascii import b2a_hex, a2b_hex
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

from autobahn.util import hltype, hlval, hlid
from autobahn.websocket.util import parse_url
from autobahn.twisted.wamp import ApplicationSession
from crossbar.common.twisted.endpoint import _create_tls_client_context

from autobahn.wamp.cryptosign import CryptosignKey
from autobahn.xbr import make_w3, EthereumKey, SecurityModuleMemory, EIP712DelegateCertificate

from autobahn.xbr import create_eip712_delegate_certificate, create_eip712_authority_certificate, \
    EIP712AuthorityCertificate


class ClientSession(ApplicationSession):

    def __init__(self, config=None):
        self.log.debug('{func} initializing component: {config}', func=hltype(self.__init__), config=config)
        ApplicationSession.__init__(self, config)
        self._gw_config = {
            'type': 'infura',
            'key': os.environ.get('WEB3_INFURA_PROJECT_ID', ''),
            'network': 'mainnet',
        }
        self._w3 = make_w3(self._gw_config)
        self._sm: SecurityModuleMemory = SecurityModuleMemory.from_seedphrase(self.config.extra['seedphrase'],
                                                                              num_eth_keys=10, num_cs_keys=6)

    @inlineCallbacks
    def _create_certificate_chain(self):
        # data needed for delegate certificate: cert1
        #
        chainId = self._w3.eth.chain_id
        verifyingContract = a2b_hex('0xf766Dc789CF04CD18aE75af2c5fAf2DA6650Ff57'[2:])
        validFrom = self._w3.eth.block_number
        delegate = self._eth_key.address(binary=True)
        csPubKey = self._key.public_key(binary=True)
        bootedAt = txaio.time_ns()
        delegateMeta = ''

        # data needed for intermediate authority certificate: cert2
        #
        issuer_cert2 = self._trustroot_eth_key.address(binary=True)
        subject_cert2 = delegate
        realm_cert2 = a2b_hex('0xA6e693CC4A2b4F1400391a728D26369D9b82ef96'[2:])
        capabilities_cert2 = EIP712AuthorityCertificate.CAPABILITY_PUBLIC_RELAY | EIP712AuthorityCertificate.CAPABILITY_PRIVATE_RELAY
        meta_cert2 = ''

        # data needed for root authority certificate: cert3
        #
        issuer_cert3 = self._trustroot_eth_key.address(binary=True)
        subject_cert3 = issuer_cert3
        realm_cert3 = realm_cert2
        capabilities_cert3 = EIP712AuthorityCertificate.CAPABILITY_ROOT_CA | EIP712AuthorityCertificate.CAPABILITY_INTERMEDIATE_CA | EIP712AuthorityCertificate.CAPABILITY_PUBLIC_RELAY | EIP712AuthorityCertificate.CAPABILITY_PRIVATE_RELAY | EIP712AuthorityCertificate.CAPABILITY_PROVIDER | EIP712AuthorityCertificate.CAPABILITY_CONSUMER
        meta_cert3 = ''

        # delegate certificate
        #
        cert1_data = create_eip712_delegate_certificate(chainId=chainId, verifyingContract=verifyingContract,
                                                        validFrom=validFrom, delegate=delegate, csPubKey=csPubKey,
                                                        bootedAt=bootedAt, meta=delegateMeta)

        # print('\n\n{}\n\n'.format(pformat(cert1_data)))

        cert1_sig = yield self._eth_key.sign_typed_data(cert1_data, binary=False)

        cert1_data['message']['csPubKey'] = b2a_hex(cert1_data['message']['csPubKey']).decode()
        cert1_data['message']['delegate'] = self._w3.toChecksumAddress(cert1_data['message']['delegate'])
        cert1_data['message']['verifyingContract'] = self._w3.toChecksumAddress(
            cert1_data['message']['verifyingContract'])

        # intermediate CA certificate
        #
        cert2_data = create_eip712_authority_certificate(chainId=chainId, verifyingContract=verifyingContract,
                                                         validFrom=validFrom, issuer=issuer_cert2,
                                                         subject=subject_cert2,
                                                         realm=realm_cert2, capabilities=capabilities_cert2,
                                                         meta=meta_cert2)

        # print('\n\n{}\n\n'.format(pformat(cert2_data)))

        cert2_sig = yield self._trustroot_eth_key.sign_typed_data(cert2_data, binary=False)

        cert2_data['message']['verifyingContract'] = self._w3.toChecksumAddress(
            cert2_data['message']['verifyingContract'])
        cert2_data['message']['issuer'] = self._w3.toChecksumAddress(cert2_data['message']['issuer'])
        cert2_data['message']['subject'] = self._w3.toChecksumAddress(cert2_data['message']['subject'])
        cert2_data['message']['realm'] = self._w3.toChecksumAddress(cert2_data['message']['realm'])

        # create root authority certificate
        #
        cert3_data = create_eip712_authority_certificate(chainId=chainId, verifyingContract=verifyingContract,
                                                         validFrom=validFrom, issuer=issuer_cert3,
                                                         subject=subject_cert3,
                                                         realm=realm_cert3, capabilities=capabilities_cert3,
                                                         meta=meta_cert3)

        cert3_sig = yield self._trustroot_eth_key.sign_typed_data(cert3_data, binary=False)

        cert3_data['message']['verifyingContract'] = self._w3.toChecksumAddress(
            cert3_data['message']['verifyingContract'])
        cert3_data['message']['issuer'] = self._w3.toChecksumAddress(cert3_data['message']['issuer'])
        cert3_data['message']['subject'] = self._w3.toChecksumAddress(cert3_data['message']['subject'])
        cert3_data['message']['realm'] = self._w3.toChecksumAddress(cert3_data['message']['realm'])

        # create certificates chain
        #
        certificates = [(cert1_data, cert1_sig), (cert2_data, cert2_sig), (cert3_data, cert3_sig)]
        return certificates

    @inlineCallbacks
    def onConnect(self):
        self.log.debug('{func} connected to router', func=hltype(self.onConnect))
        try:
            assert self._w3.isConnected()

            yield self._sm.open()

            # Ethereum key pairs
            root_ca1_ekey: EthereumKey = self._sm[1]
            relay_ep1_ekey: EthereumKey = self._sm[6]

            # Cryptosign key pairs
            relay_dl1_ckey: CryptosignKey = self._sm[10]

            # ######## delegate ("node") certificate ############################################
            relay_dl1_cert_chainId = self._w3.eth.chain_id
            relay_dl1_cert_verifyingContract = a2b_hex('0xf766Dc789CF04CD18aE75af2c5fAf2DA6650Ff57'[2:])
            relay_dl1_cert_validFrom = self._w3.eth.block_number
            relay_dl1_cert_meta = ''
            relay_dl1_cert_bootedAt = txaio.time_ns()
            relay_dl1_cert = EIP712DelegateCertificate(chainId=relay_dl1_cert_chainId,
                                                       verifyingContract=relay_dl1_cert_verifyingContract,
                                                       validFrom=relay_dl1_cert_validFrom,
                                                       delegate=relay_ep1_ekey.address(binary=True),
                                                       csPubKey=relay_dl1_ckey.public_key(binary=True),
                                                       bootedAt=relay_dl1_cert_bootedAt,
                                                       meta=relay_dl1_cert_meta)
            relay_dl1_cert_sig = yield relay_dl1_cert.sign(relay_ep1_ekey, binary=False)
            log.info(
                'EIP712DelegateCertificate issued by delegate {delegate} for csPubKey {csPubKey} and bootedAt {bootedAt}',
                delegate=self._w3.toChecksumAddress(relay_dl1_cert.delegate),
                csPubKey=binascii.b2a_hex(relay_dl1_cert.csPubKey).decode(),
                bootedAt=relay_dl1_cert_bootedAt)

            # certificates = yield self._create_certificate_chain()
            certificates = [(relay_dl1_cert.marshal(), relay_dl1_cert_sig)]

            # authentication extra information for wamp-cryptosign
            authextra = {
                # forward the client pubkey: required!
                'pubkey': relay_dl1_ckey.public_key(binary=False),

                # when running over TLS, require TLS channel binding
                'channel_binding': self.config.extra['channel_binding'],

                # not yet implemented. a public key the router should provide
                # a trust chain for its public key. the trustroot can e.g. be
                # hard-coded in the client, or come from a command line option.
                # 'trustroot': self.config.extra['trustroot'],
                'trustroot': root_ca1_ekey.address(binary=False),

                # certificate chain beginning with delegate certificate for this client (the delegate)
                'certificates': certificates,

                # for authenticating the router, this challenge will need to be signed by
                # the router and send back in AUTHENTICATE for client to verify.
                # A string with a hex encoded 32 bytes random value.
                'challenge': self.config.extra['challenge'],
            }
            self.log.debug('authenticating using authextra:\n\n{authextra}\n', authextra=pformat(authextra))

            # now request to join
            self.join(self.config.realm, authmethods=['cryptosign'], authextra=authextra)
        except:
            self.log.failure()
            raise

    def onChallenge(self, challenge):
        self.log.debug('{func} authentication challenge received: {challenge}',
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
            assert len(signature) == 96, 'unexpected length {} of signature'.format(len(signature))
            try:
                verify_key.verify(signature)
            except BadSignatureError:
                raise RuntimeError('invalid router signature for client challenge')
            else:
                self.log.debug('{func} ok, successfully verified router signature for router public key {pubkey}',
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
        self.log.debug('{func} session joined: {details}', func=hltype(self.onJoin), details=details)
        self.log.info(hlval('*' * 80, color='green', bold=True))
        self.log.info(
            '{action}:\n\n    realm="{realm}"\n    authrole="{authrole}"\n    authid="{authid}"\n',
            action=hlval('OK, successfully authenticated with WAMP-cryptosign', color='green', bold=True),
            realm=hlid(details.realm), authid=hlid(details.authid), authrole=hlid(details.authrole))
        self.log.info(hlval('*' * 80, color='green', bold=True))

        # alright, nothing more to do: leave again
        self.leave()

    @inlineCallbacks
    def onLeave(self, details):
        self.log.debug("{func} session closed: {details}", func=hltype(self.onLeave), details=details)
        self.config.extra['exit_details'] = details

        # close security module
        yield self._sm.close()

        # disconnect from router
        self.disconnect()

    def onDisconnect(self):
        self.log.debug('{func} connection to router closed', func=hltype(self.onDisconnect))
        try:
            reactor.stop()
        except ReactorNotRunning:
            pass


if __name__ == '__main__':

    # parse command line arguments
    parser = argparse.ArgumentParser()

    parser.add_argument('--debug', dest='debug', action='store_true',
                        default=False, help='Enable logging at level "debug".')

    parser.add_argument('--seedphrase', dest='seedphrase', type=str,
                        default="avocado style uncover thrive same grace crunch want essay reduce current edge",
                        help='Seedphrase to generate security module keys from (both Ethereum and Cryptosign)')

    parser.add_argument('--channel_binding', dest='channel_binding', type=str, default=None,
                        help='Optional TLS channel binding, e.g. "tls-unique"')
    parser.add_argument('--trustroot', dest='trustroot', type=str, default=None,
                        help='Optional client trustroot, e.g. "0xf766Dc789CF04CD18aE75af2c5fAf2DA6650Ff57"')
    parser.add_argument('--challenge', dest='challenge', action='store_true',
                        default=False, help='Enable router challenge.')

    parser.add_argument('--url', dest='url', type=str, default='wss://localhost:8080/ws',
                        help='The router URL (default: wss://localhost:8080/ws).')
    parser.add_argument('--realm', dest='realm', type=str, default='realm1',
                        help='The realm to join. If not provided, let the router auto-choose the realm.')
    parser.add_argument('--authid', dest='authid', type=str, default=None,
                        help='The authid to connect under. If not provided, let the router auto-choose the authid.')

    options = parser.parse_args()

    if options.debug:
        # txaio.start_logging(level='debug')
        txaio.start_logging(level='trace')
    else:
        txaio.start_logging(level='info')
    log = make_logger()

    isSecure, host, uds_path, resource, path, params = parse_url(options.url)

    # forward requested authid and key filename to ClientSession
    extra = {
        'channel_binding': options.channel_binding,
        'trustroot': options.trustroot,
        'challenge': binascii.b2a_hex(os.urandom(32)).decode() if options.challenge else None,
        'authid': options.authid,
        'seedphrase': options.seedphrase,
        'run_details': {
            'tls_transport': isSecure,
            'tls_channel_binding': options.channel_binding,
            'router_challenge': options.challenge,

        },
        'exit_details': None,
    }

    if isSecure:
        tls_config = {
            "hostname": host,
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
    else:
        cert_options = None

    # connect to router and run ClientSession
    runner = ApplicationRunner(
        url=options.url, realm=options.realm, extra=extra, ssl=cert_options)
    runner.run(ClientSession)

    print('\nRun details:\n')
    pprint(extra['run_details'])
    print()

    if extra['exit_details'].reason != 'wamp.close.normal':
        print(extra['exit_details'])
        sys.exit(1)
    else:
        sys.exit(0)
