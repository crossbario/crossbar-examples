import binascii
import os
from uuid import UUID

import txaio
txaio.use_twisted()

from autobahn.twisted.component import Component, run
from autobahn.twisted.util import sleep
from autobahn.twisted.xbr import SimpleSeller
from autobahn.wamp.types import PublishOptions

market_maker_adr = os.environ.get('XBR_MARKET_MAKER_ADR', '0x3e5e9111ae8eb78fe1cc3bb8915d5d461f3ef9a9')
print('market_maker_adr', market_maker_adr)
market_maker_adr = binascii.a2b_hex(market_maker_adr[2:])

seller_priv_key = os.environ.get('XBR_SELLER_PRIVKEY', '0xadd53f9a7e588d003326d1cbf9e4a43c061aadd9bc938c843a79e7b4fd2ad743')
print('seller_priv_key', seller_priv_key)
seller_priv_key = binascii.a2b_hex(seller_priv_key[2:])


comp = Component(
    transports=os.environ.get('XBR_INSTANCE', 'ws://edge1:8080/ws'),
    realm=os.environ.get('XBR_REALM', 'realm1'),
    extra={
        'market_maker_adr': market_maker_adr,
        'seller_privkey': seller_priv_key,
    }
)


running = False


@comp.on_join
async def joined(session, details):
    print('Seller session joined', details)
    global running
    running = True

    # market_maker_adr = binascii.a2b_hex(session.config.extra['market_maker_adr'][2:])
    market_maker_adr = session.config.extra['market_maker_adr']
    print('Using market maker adr:', session.config.extra['market_maker_adr'])

    # seller_privkey = binascii.a2b_hex(session.config.extra['seller_privkey'][2:])
    seller_privkey = session.config.extra['seller_privkey']

    api_id = UUID('627f1b5c-58c2-43b1-8422-a34f7d3f5a04').bytes
    topic = 'io.crossbar.example'
    counter = 1

    seller = SimpleSeller(market_maker_adr, seller_privkey)
    price = 35 * 10 ** 18
    interval = 10
    seller.add(api_id, topic, price, interval, None)

    balance = await seller.start(session)
    balance = int(balance / 10 ** 18)
    print("Remaining balance: {} XBR".format(balance))

    while running:
        payload = {'data': 'py-seller', 'counter': counter}
        key_id, enc_ser, ciphertext = await seller.wrap(api_id,
                                                        topic,
                                                        payload)

        pub = await session.publish(topic, key_id, enc_ser, ciphertext,
                                    options=PublishOptions(acknowledge=True))

        print('Published event {}: {}'.format(pub.id, payload))

        counter += 1
        await sleep(1)


@comp.on_leave
def left(session, details):
    print('Seller session left', details)
    global running
    running = False


if __name__ == '__main__':
    run([comp])
