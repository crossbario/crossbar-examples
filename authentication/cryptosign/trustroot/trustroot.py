import os
import argparse
from pprint import pformat
from binascii import a2b_hex, b2a_hex

import txaio
txaio.use_twisted()

from txaio import make_logger
from twisted.internet import task

from autobahn.wamp.cryptosign import CryptosignKey
from autobahn.xbr import EthereumKey
from autobahn.xbr._secmod import SecurityModuleMemory
from autobahn.xbr._eip712_delegate_certificate import create_eip712_delegate_certificate


async def main(reactor, log, trustroot_keyfile, keyfile, certfile):
    sm_trustroot = SecurityModuleMemory.from_keyfile(trustroot_keyfile)
    await sm_trustroot.open()

    assert isinstance(sm_trustroot[0], EthereumKey)
    assert isinstance(sm_trustroot[1], CryptosignKey)
    log.info('Loaded trustroot EthereumKey {address}', address=sm_trustroot[0].address(binary=False))
    log.info('Loaded trustroot CryptosignKey {pubkey}', pubkey=sm_trustroot[1].public_key(binary=False))

    eth_key = EthereumKey.from_keyfile(keyfile)
    log.info('Loaded EthereumKey to be signed with {address}', address=eth_key.address(binary=False))

    chainId = 1
    validFrom = 1
    verifyingContract = a2b_hex('0xf766Dc789CF04CD18aE75af2c5fAf2DA6650Ff57'[2:])
    delegate = a2b_hex('0x2F070c2f49a59159A0346396f1139203355ACA43'[2:])
    csPubKey = a2b_hex('a57b7b84ee17f60f77bfaaf84ba74858884cd30c9868dac40dd9cc90fab3bf9d')
    csChallenge = a2b_hex('eb870538efe96311e4cd9b18947bbff491d5d31a7b292c5b6ca48f6ad24f16dd')
    csChannelId = a2b_hex('70f1c7ecaf43858f256d45c4c5db76a2b1b2c18c418fc828600f1ce9e1f71ce1')
    reservation = a2b_hex('0xe78ea2fE1533D4beD9A10d91934e109A130D0ad8'[2:])

    cert_data = create_eip712_delegate_certificate(chainId=chainId, verifyingContract=verifyingContract,
                                                   validFrom=validFrom, delegate=delegate, csPubKey=csPubKey,
                                                   csChallenge=csChallenge, csChannelId=csChannelId,
                                                   reservation=reservation)

    log.info('signing certificate data:\n{cert_data}', cert_data=pformat(cert_data))

    cert_sig = await sm_trustroot[0].sign_typed_data(cert_data, binary=False)
    log.info('signature: {cert_sig}', cert_sig=cert_sig)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--debug', dest='debug', action='store_true',
                        default=False, help='Enable logging at level "debug".')
    parser.add_argument('--trustroot-keyfile', dest='trustroot_keyfile', type=str, required=True,
                        help='The keyfile to use for the trustroot to sign certificates.')
    parser.add_argument('--keyfile', dest='keyfile', type=str, required=True,
                        help='The keyfile with keys to sign and create certificates for.')
    parser.add_argument('--certfile', dest='certfile', type=str, required=True,
                        help='The certificate file to create.')
    options = parser.parse_args()

    if options.debug:
        txaio.start_logging(level='debug')
    else:
        txaio.start_logging(level='info')
    log = make_logger()

    task.react(main, (log, options.trustroot_keyfile, options.keyfile, options.certfile))
