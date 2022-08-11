import binascii
import os
import argparse
from binascii import a2b_hex

import txaio

txaio.use_twisted()

from txaio import make_logger
from twisted.internet import task

from autobahn.wamp.cryptosign import CryptosignKey
from autobahn.xbr import make_w3, EthereumKey, SecurityModuleMemory, EIP712AuthorityCertificate, EIP712DelegateCertificate


async def main(reactor, log, gw_config, seedphrase, outdir, realm):
    # blockchain gateway
    w3 = make_w3(gw_config)

    # security module to use: in-memory module initialized with keyring generated from seedphrase
    sm: SecurityModuleMemory = SecurityModuleMemory.from_seedphrase(seedphrase, num_eth_keys=10, num_cs_keys=6)
    await sm.open()

    # Ethereum key pairs
    unused_1: EthereumKey = sm[0]
    root_ca1_ekey: EthereumKey = sm[1]
    relay_ca1_ekey: EthereumKey = sm[2]
    relay_ca2_ekey: EthereumKey = sm[3]
    gateway_ca1_ekey: EthereumKey = sm[4]
    gateway_ca2_ekey: EthereumKey = sm[5]
    relay_ep1_ekey: EthereumKey = sm[6]
    relay_ep2_ekey: EthereumKey = sm[7]
    gateway_ep1_ekey: EthereumKey = sm[8]
    gateway_ep2_ekey: EthereumKey = sm[9]

    # Cryptosign key pairs
    relay_dl1_ckey: CryptosignKey = sm[10]
    relay_dl2_ckey: CryptosignKey = sm[11]
    gateway_dl1_ckey: CryptosignKey = sm[12]
    gateway_dl2_ckey: CryptosignKey = sm[13]
    unused_2: CryptosignKey = sm[14]
    unused_3: CryptosignKey = sm[15]

    # assemble data used in all generated certificates
    cert_chainId = w3.eth.chain_id
    cert_verifyingContract = a2b_hex('0xf766Dc789CF04CD18aE75af2c5fAf2DA6650Ff57'[2:])
    cert_realm = a2b_hex(realm[2:])
    cert_validFrom = w3.eth.block_number
    cert_meta = ''

    # ######## root CA ("realm owner") certificate ######################################
    root_ca1_cert_filename = os.path.join(outdir, 'root_ca1.crt')
    root_ca1_cert = EIP712AuthorityCertificate(chainId=cert_chainId,
                                               verifyingContract=cert_verifyingContract,
                                               validFrom=cert_validFrom,
                                               issuer=root_ca1_ekey.address(binary=True),
                                               subject=root_ca1_ekey.address(binary=True),
                                               realm=cert_realm,
                                               capabilities=EIP712AuthorityCertificate.CAPABILITY_ROOT_CA | EIP712AuthorityCertificate.CAPABILITY_INTERMEDIATE_CA | EIP712AuthorityCertificate.CAPABILITY_PUBLIC_RELAY | EIP712AuthorityCertificate.CAPABILITY_PRIVATE_RELAY | EIP712AuthorityCertificate.CAPABILITY_PROVIDER | EIP712AuthorityCertificate.CAPABILITY_CONSUMER,
                                               meta=cert_meta)
    root_ca1_cert_sig = await root_ca1_cert.sign(root_ca1_ekey, binary=True)
    root_ca1_cert.signatures = [root_ca1_cert_sig]
    root_ca1_cert.save(root_ca1_cert_filename)
    log.info('EIP712AuthorityCertificate issued by {issuer} for subject {subject} saved to "{filename}"',
             issuer=w3.toChecksumAddress(root_ca1_cert.issuer),
             subject=w3.toChecksumAddress(root_ca1_cert.subject),
             filename=root_ca1_cert_filename)

    # ######## intermediate CA ("operator") certificate #################################
    relay_ca1_cert_filename = os.path.join(outdir, 'relay_ca1.crt')
    relay_ca1_cert = EIP712AuthorityCertificate(chainId=cert_chainId,
                                                verifyingContract=cert_verifyingContract,
                                                validFrom=cert_validFrom,
                                                issuer=root_ca1_ekey.address(binary=True),
                                                subject=relay_ca1_ekey.address(binary=True),
                                                realm=cert_realm,
                                                capabilities=EIP712AuthorityCertificate.CAPABILITY_INTERMEDIATE_CA | EIP712AuthorityCertificate.CAPABILITY_PUBLIC_RELAY | EIP712AuthorityCertificate.CAPABILITY_PRIVATE_RELAY | EIP712AuthorityCertificate.CAPABILITY_PROVIDER | EIP712AuthorityCertificate.CAPABILITY_CONSUMER,
                                                meta=cert_meta)
    relay_ca1_cert_sig = await relay_ca1_cert.sign(relay_ca1_ekey, binary=True)
    relay_ca1_cert.signatures = [relay_ca1_cert_sig]
    relay_ca1_cert.save(relay_ca1_cert_filename)
    log.info('EIP712AuthorityCertificate issued by {issuer} for subject {subject} saved to "{filename}"',
             issuer=w3.toChecksumAddress(relay_ca1_cert.issuer),
             subject=w3.toChecksumAddress(relay_ca1_cert.subject),
             filename=relay_ca1_cert_filename)

    # ######## endpoint ("node") certificate ############################################
    relay_ep1_cert_filename = os.path.join(outdir, 'relay_ep1.crt')
    relay_ep1_cert = EIP712AuthorityCertificate(chainId=cert_chainId,
                                                verifyingContract=cert_verifyingContract,
                                                validFrom=cert_validFrom,
                                                issuer=relay_ca1_ekey.address(binary=True),
                                                subject=relay_ep1_ekey.address(binary=True),
                                                realm=cert_realm,
                                                capabilities=EIP712AuthorityCertificate.CAPABILITY_PUBLIC_RELAY | EIP712AuthorityCertificate.CAPABILITY_PRIVATE_RELAY,
                                                meta=cert_meta)
    relay_ep1_cert_sig = await relay_ep1_cert.sign(relay_ca1_ekey, binary=True)
    relay_ep1_cert.signatures = [relay_ep1_cert_sig]
    relay_ep1_cert.save(relay_ep1_cert_filename)
    log.info('EIP712AuthorityCertificate issued by {issuer} for subject {subject} saved to "{filename}"',
             issuer=w3.toChecksumAddress(relay_ep1_cert.issuer),
             subject=w3.toChecksumAddress(relay_ep1_cert.subject),
             filename=relay_ep1_cert_filename)

    # close security module
    await sm.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('--debug', dest='debug', action='store_true',
                        default=False, help='Enable logging at level "debug".')
    parser.add_argument('--seedphrase', dest='seedphrase', type=str,
                        default="avocado style uncover thrive same grace crunch want essay reduce current edge",
                        help='BIP-39 seedphrase ("Mnemonic") to generate security module keys from (both Ethereum and Cryptosign)')
    parser.add_argument('--outdir', dest='outdir', type=str, required=True,
                        help='Output directory for certificates.')
    parser.add_argument('--realm', dest='realm', type=str, required=True,
                        help='realm')

    options = parser.parse_args()

    if options.debug:
        txaio.start_logging(level='debug')
    else:
        txaio.start_logging(level='info')
    _log = make_logger()

    _gw_config = {
        'type': 'infura',
        'key': os.environ.get('WEB3_INFURA_PROJECT_ID', ''),
        'network': 'mainnet',
    }

    task.react(main, (_log, _gw_config, options.seedphrase, options.outdir, options.realm))
