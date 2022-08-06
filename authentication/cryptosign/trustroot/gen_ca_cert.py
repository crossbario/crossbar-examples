import os
import argparse
from binascii import a2b_hex

import txaio
txaio.use_twisted()

from txaio import make_logger
from twisted.internet import task

from autobahn.xbr import make_w3, EthereumKey
from autobahn.xbr._secmod import SecurityModuleMemory
from autobahn.xbr import EIP712AuthorityCertificate


async def main(reactor, log, seedphrase, filename, keyno, verifyingContract, realm):
    gw_config = {
        'type': 'infura',
        'key': os.environ.get('WEB3_INFURA_PROJECT_ID', ''),
        'network': 'mainnet',
    }
    w3 = make_w3(gw_config)

    hsm: SecurityModuleMemory = SecurityModuleMemory.from_seedphrase(seedphrase, num_eth_keys=5, num_cs_keys=5)
    await hsm.open()

    # keys needed to create all certificates in certificate chain
    ca_key: EthereumKey = hsm[keyno]

    # data needed for root authority certificate: cert3
    ca_cert_chainId = w3.eth.chain_id
    ca_cert_verifyingContract = a2b_hex(verifyingContract[2:])  # a2b_hex('0xf766Dc789CF04CD18aE75af2c5fAf2DA6650Ff57'[2:])
    ca_cert_validFrom = w3.eth.block_number
    ca_cert_issuer = ca_key.address(binary=True)
    ca_cert_subject = ca_cert_issuer
    ca_cert_realm = a2b_hex(realm[2:])  # a2b_hex('0xA6e693CC4A2b4F1400391a728D26369D9b82ef96'[2:])
    ca_cert_capabilities = EIP712AuthorityCertificate.CAPABILITY_ROOT_CA | EIP712AuthorityCertificate.CAPABILITY_INTERMEDIATE_CA | EIP712AuthorityCertificate.CAPABILITY_PUBLIC_RELAY | EIP712AuthorityCertificate.CAPABILITY_PRIVATE_RELAY | EIP712AuthorityCertificate.CAPABILITY_PROVIDER | EIP712AuthorityCertificate.CAPABILITY_CONSUMER
    ca_cert_meta = ''

    # create root authority certificate
    ca_cert = EIP712AuthorityCertificate(chainId=ca_cert_chainId,
                                         verifyingContract=ca_cert_verifyingContract,
                                         validFrom=ca_cert_validFrom,
                                         issuer=ca_cert_issuer,
                                         subject=ca_cert_subject,
                                         realm=ca_cert_realm,
                                         capabilities=ca_cert_capabilities,
                                         meta=ca_cert_meta)
    ca_cert_sig = await ca_cert.sign(ca_key, binary=True)
    ca_cert.save(filename, ca_cert_sig)

    log.info('root CA certificate:\n\n{cert_data}\n', cert_data=ca_cert)
    log.info('root CA issuer {issuer} certificate saved to:\n\n{filename}\n',
             issuer=w3.toChecksumAddress(ca_cert.issuer),
             filename=filename)

    await hsm.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--debug', dest='debug', action='store_true',
                        default=False, help='Enable logging at level "debug".')
    parser.add_argument('--seedphrase', dest='seedphrase', type=str,
                        default="avocado style uncover thrive same grace crunch want essay reduce current edge",
                        help='BIP-39 seedphrase ("Mnemonic") to generate security module keys from (both Ethereum and Cryptosign)')
    parser.add_argument('--keyno', dest='keyno', type=int, required=True,
                        help='Key number from BIP-39 key ring generated from seedphrase.')
    parser.add_argument('--certfile', dest='certfile', type=str, required=True,
                        help='Output filename for certificate.')

    parser.add_argument('--verifyingContract', dest='verifyingContract', type=str, required=True,
                        help='verifyingContract')
    parser.add_argument('--realm', dest='realm', type=str, required=True,
                        help='realm')

    options = parser.parse_args()

    if options.debug:
        txaio.start_logging(level='debug')
    else:
        txaio.start_logging(level='info')
    log = make_logger()

    task.react(main, (log, options.seedphrase, options.certfile, options.keyno, options.verifyingContract, options.realm))
