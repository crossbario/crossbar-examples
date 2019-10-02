import binascii
import os

import txaio
txaio.use_twisted()

from autobahn.wamp.types import SubscribeOptions
from autobahn.twisted.component import Component, run
from autobahn.twisted.xbr import SimpleBuyer

comp = Component(
    transports=os.environ.get('XBR_INSTANCE', 'ws://edge1:8080/ws'),
    realm=os.environ.get('XBR_REALM', 'realm1'),
    extra={
        'market_maker_adr': os.environ.get('XBR_MARKET_MAKER_ADR', '0x3e5e9111ae8eb78fe1cc3bb8915d5d461f3ef9a9'),
        'buyer_privkey': os.environ.get('XBR_BUYER_PRIVKEY', '0x395df67f0c2d2d9fe1ad08d1bc8b6627011959b79c53d7dd6a3536a33ab8a4fd'),
    }
)


@comp.on_join
async def joined(session, details):
    print('Buyer session joined', details)

    market_maker_adr = binascii.a2b_hex(session.config.extra['market_maker_adr'][2:])
    print('Using market maker adr:', session.config.extra['market_maker_adr'])

    buyer_privkey = binascii.a2b_hex(session.config.extra['buyer_privkey'][2:])

    max_price = 100 * 10 ** 18
    buyer = SimpleBuyer(market_maker_adr, buyer_privkey, max_price)
    balance = await buyer.start(session, details.authid)
    balance = int(balance / 10 ** 18)
    print("Remaining balance: {} XBR".format(balance))

    async def on_event(key_id, enc_ser, ciphertext, details=None):
        try:
            print('Received encrypted event {} ..'.format(details.publication))
            payload = await buyer.unwrap(key_id, enc_ser, ciphertext)
        except Exception as e:
            print(e)
            session.leave()
        else:
            print('Decrypted event {} payload:'.format(details.publication), payload)

    await session.subscribe(on_event, "io.crossbar.example", options=SubscribeOptions(details=True))


if __name__ == '__main__':
    run([comp])
