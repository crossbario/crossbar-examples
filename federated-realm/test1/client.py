import os
from binascii import b2a_hex
from random import randint

import txaio
txaio.use_twisted()

from twisted.internet.defer import inlineCallbacks
from autobahn.twisted.util import sleep
from autobahn.util import hltype, hlval
from autobahn.twisted.component import Component, run
from autobahn.wamp.types import PublishOptions
from autobahn.wamp.exception import ApplicationError
from autobahn.wamp.message import identity_realm_name_category

log = txaio.make_logger()


@inlineCallbacks
def main(reactor, session):
    log.info('{func} session connected.\nsession_details=\n{session_details}\transport_details={transport_details}',
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

    # privkey = '20e8c05d0ede9506462bb049c4843032b18e8e75b314583d0c8d8a4942f9be40'
    # privkey = b2a_hex(os.urandom(32)).decode()

    privkey = 'a8ab7ca271bf9e5f38f307687dbc89c1f9a4f24d53fb497484f17577b4876caf'
    pubkey = '0e006ab034449502377f0d0147150f9f19275ddc56c8b274e97742a42ffacc49'
    log.info('using privkey=0x{privkey}', privkey=hlval(privkey))
    log.info('using pubkey=0x{pubkey}', pubkey=hlval(pubkey))

    # realm = 'realm1'
    realm = 'wamp-proto.eth'

    realm_category = identity_realm_name_category(realm)
    log.info('realm name "{realm}" is of category {realm_category}',
             realm=hlval(realm), realm_category=hlval(realm_category))

    # https://github.com/crossbario/crossbar/blob/95b30b1a03e9596191887af2738f04b9624ff11b/crossbar/worker/rlink.py#L542

    authentication = {
        'cryptosign': {
            'privkey': privkey,
            'authextra': {
                # forward the client pubkey: this allows us to omit authid as
                # the router can identify us with the pubkey already
                'pubkey': pubkey,

                # not yet implemented. a public key the router should provide
                # a trustchain for its public key. the trustroot can eg be
                # hard-coded in the client, or come from a command line option.
                'trustroot': None,

                # not yet implemented. for authenticating the router, this
                # challenge will need to be signed by the router and send back
                # in AUTHENTICATE for client to verify. A string with a hex
                # encoded 32 bytes random value.
                'challenge': None,

                # https://tools.ietf.org/html/rfc5929
                # 'channel_binding': 'tls-unique'
                'channel_binding': None,

                'operator': '0xe59C7418403CF1D973485B36660728a5f4A8fF9c',
                'request_bandwidth': 100,
            }
        }
    }

    component = Component(transports=transports,
                          main=main,
                          realm=realm,
                          authentication=authentication)
    run([component])
