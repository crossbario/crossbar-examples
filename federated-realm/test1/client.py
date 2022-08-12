import os
from binascii import b2a_hex, a2b_hex
from random import randint

import txaio
txaio.use_twisted()

from twisted.internet.defer import inlineCallbacks
from autobahn.twisted.util import sleep
from autobahn.util import hltype, hlval
from autobahn.twisted.component import Component, run
from autobahn.wamp.types import PublishOptions
from autobahn.wamp.exception import ApplicationError
from autobahn.wamp.message import identify_realm_name_category
from autobahn.wamp.cryptosign import CryptosignKey
from autobahn.wamp.interfaces import ICryptosignKey, IEthereumKey

log = txaio.make_logger()


@inlineCallbacks
def main(reactor, session):
    log.info('{func} session connected.\nsession_details=\n{session_details}\ntransport_details=\n{transport_details}',
             session_details=session.session_details,
             transport_details=session.transport.transport_details,
             func=hltype(main))
    while session.is_attached():
        x = randint(0, 2**16)
        y = randint(0, 2**16)
        s = yield session.call('user.add2', x, y)
        assert s == x + y
        sq = s * s
        pub = yield session.publish('user.on_square', sq, options=PublishOptions(acknowledge=True))
        log.info('{func} published event {pub_id}: sq={sq}',
                 func=hltype(main),
                 sq=hlval(sq),
                 pub_id=hlval(pub.id))
        yield sleep(1)


if __name__ == "__main__":
    # transports = os.environ.get('WAMP_ROUTER_URLS', '').split(',')
    transports = ['ws://localhost:8080/ws', 'ws://localhost:8081/ws', 'ws://localhost:8082/ws']
    # transports = ['ws://localhost:8080/ws']

    # public-adr-eth: 0xe59C7418403CF1D973485B36660728a5f4A8fF9c
    # private-key-eth: 6b08b6e186bd2a3b9b2f36e6ece3f8031fe788ab3dc4a1cfd3a489ea387c496b

    # privkey = b2a_hex(os.urandom(32)).decode()

    client_key_hex = '20e8c05d0ede9506462bb049c4843032b18e8e75b314583d0c8d8a4942f9be40'
    client_key: ICryptosignKey = CryptosignKey.from_bytes(a2b_hex(client_key_hex))
    log.info('using client_key:\nprivkey=0x{privkey}\npubkey=0x{pubkey}',
             privkey=hlval(client_key_hex),
             pubkey=hlval(client_key.public_key(binary=False)))

    delegate_key_hex = '6b08b6e186bd2a3b9b2f36e6ece3f8031fe788ab3dc4a1cfd3a489ea387c496b'
    delegate_key: IEthereumKey = None
    log.info('using delegate_key:\nseed=0x{seed}\naddress=0x{address}',
             seed=hlval(delegate_key_hex),
             address=hlval(delegate_key.address(binary=False)))

    # realm = 'realm1'
    realm = 'wamp-proto.eth'

    realm_category = identify_realm_name_category(realm)
    log.info('realm name "{realm}" is of category {realm_category}',
             realm=hlval(realm), realm_category=hlval(realm_category))

    # https://github.com/crossbario/crossbar/blob/95b30b1a03e9596191887af2738f04b9624ff11b/crossbar/worker/rlink.py#L542

    authentication = {
        'cryptosign': {
            'privkey': client_key_hex,
            'authextra': {
                # forward the client pubkey: this allows us to omit authid as
                # the router can identify us with the pubkey already
                # 'pubkey': pubkey,

                # not yet implemented. a public key the router should provide
                # a trustchain for its public key. the trustroot can eg be
                # hard-coded in the client, or come from a command line option.
                'trustroot': None,

                # not yet implemented. for authenticating the router, this
                # challenge will need to be signed by the router and send back
                # in AUTHENTICATE for client to verify. A string with a hex
                # encoded 32 bytes random value.
                # 'challenge': None,

                # int
                'chain_id': None,

                # int
                'block_no': None,

                # string
                'channel_binding': 'tls-unique',

                # string
                'channel_id': None,

                # string
                'challenge': None,

                # address
                'operator': '0xe59C7418403CF1D973485B36660728a5f4A8fF9c',

                # address
                'realm': None,

                # string
                'pubkey': client_key.public_key(binary=False),

                # int
                'bandwidth': 100,

                # string
                'signature': None,
            }
        }
    }

    component = Component(transports=transports,
                          main=main,
                          realm=realm,
                          authentication=authentication)
    run([component])
