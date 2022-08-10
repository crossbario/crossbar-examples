import os
import argparse
from binascii import a2b_hex

import txaio

txaio.use_twisted()

from txaio import make_logger
from twisted.internet import task

from autobahn.wamp.cryptosign import CryptosignKey
from autobahn.xbr import make_w3, EthereumKey, SecurityModuleMemory, EIP712AuthorityCertificate


async def main(reactor, log, gw_config, seedphrase, filename, realm):
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
    relay_ep1_ckey: CryptosignKey = sm[10]
    relay_ep2_ckey: CryptosignKey = sm[11]
    gateway_ep1_ckey: CryptosignKey = sm[12]
    gateway_ep2_ckey: CryptosignKey = sm[13]
    unused_2: CryptosignKey = sm[14]
    unused_3: CryptosignKey = sm[15]

    # assemble data used in all generated certificates
    cert_chainId = w3.eth.chain_id
    cert_verifyingContract = a2b_hex('0xf766Dc789CF04CD18aE75af2c5fAf2DA6650Ff57'[2:])
    cert_realm = a2b_hex(realm[2:])

    # ######## root CA ("realm owner") certificate ######################################

    # assemble data needed for root CA certificate
    root_ca1_cert_validFrom = w3.eth.block_number
    root_ca1_cert_issuer = root_ca1_ekey.address(binary=True)
    root_ca1_cert_subject = root_ca1_cert_issuer
    root_ca1_cert_capabilities = EIP712AuthorityCertificate.CAPABILITY_ROOT_CA | EIP712AuthorityCertificate.CAPABILITY_INTERMEDIATE_CA | EIP712AuthorityCertificate.CAPABILITY_PUBLIC_RELAY | EIP712AuthorityCertificate.CAPABILITY_PRIVATE_RELAY | EIP712AuthorityCertificate.CAPABILITY_PROVIDER | EIP712AuthorityCertificate.CAPABILITY_CONSUMER
    root_ca1_cert_meta = ''

    # create root CA certificate
    root_ca1_cert = EIP712AuthorityCertificate(chainId=cert_chainId,
                                               verifyingContract=cert_verifyingContract,
                                               validFrom=root_ca1_cert_validFrom,
                                               issuer=root_ca1_cert_issuer,
                                               subject=root_ca1_cert_subject,
                                               realm=cert_realm,
                                               capabilities=root_ca1_cert_capabilities,
                                               meta=root_ca1_cert_meta)

    # sign root CA certificate
    root_ca1_cert_sig = await root_ca1_cert.sign(root_ca1_ekey, binary=True)

    # save root CA certificate (with signature) to file
    root_ca1_cert.save(filename, root_ca1_cert_sig)

    log.info('root CA certificate:\n\n{cert_data}\n', cert_data=root_ca1_cert)
    log.info('root CA issuer {issuer} certificate saved to:\n\n{filename}\n',
             issuer=w3.toChecksumAddress(root_ca1_cert.issuer),
             filename=filename)

    # ######## intermediate CA ("operator") certificate #################################

    # ######## intermediate endpoint ("node") certificate ###############################

    # ######## delegate ("node") certificate ############################################

    # close security module
    await sm.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('--debug', dest='debug', action='store_true',
                        default=False, help='Enable logging at level "debug".')
    parser.add_argument('--seedphrase', dest='seedphrase', type=str,
                        default="avocado style uncover thrive same grace crunch want essay reduce current edge",
                        help='BIP-39 seedphrase ("Mnemonic") to generate security module keys from (both Ethereum and Cryptosign)')
    parser.add_argument('--certfile', dest='certfile', type=str, required=True,
                        help='Output filename for certificate.')
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

    task.react(main, (_log, _gw_config, options.seedphrase, options.certfile, options.realm))
