import os
import sys
import web3
import six

import txaio
txaio.use_twisted()

from autobahn import xbr
import argparse
from binascii import a2b_hex, b2a_hex

import txaio
from autobahn.twisted.wamp import ApplicationSession, ApplicationRunner

from init_data import ACCOUNTS, OWNER, MARKETS
from cfxdb import unpack_uint256


class MarketMakerClient(ApplicationSession):

    async def onJoin(self, details):
        self.log.debug('{klass}.onJoin(details.session={session}, details.authid="{authid}")',
                       klass=self.__class__.__name__, session=details.session, authid=details.authid)

        self.log.info('-' * 120)
        self.log.info('Channels in market (off-chain information):')
        for channel_adr, channel_type, channel_state in self.config.extra.get('channels', []):
            channel_adr = a2b_hex(channel_adr[2:])
            try:
                # get real-time off-chain channel balance (as maintained within the market maker)
                if channel_type == 1:
                    channel = await self.call('xbr.marketmaker.get_payment_channel', channel_adr)
                    balance = await self.call('xbr.marketmaker.get_payment_channel_balance', channel_adr)
                elif channel_type == 2:
                    channel = await self.call('xbr.marketmaker.get_paying_channel', channel_adr)
                    balance = await self.call('xbr.marketmaker.get_paying_channel_balance', channel_adr)
            except:
                self.log.failure()
            else:
                # initial on-chain channel amount
                amount = int(unpack_uint256(channel['amount']) / 10 ** 18)
                remaining = int(unpack_uint256(balance['remaining']) / 10 ** 18)

                ctype = {0: 'No Channel', 1: 'Payment Channel', 2: 'Paying Channel'}.get(channel['type'], 'UNKNOWN')
                cstate = {0: None, 1: 'OPEN', 2: 'CLOSING', 3: 'CLOSED', 4: 'FAILED'}.get(channel['state'], 'UNKNOWN')

                print('    {} 0x{}: market {}, delegate {}, currently in {} state, initial amount {} XBR, current off-chain balance {} XBR'.format(ctype,
                                                                                                                                                   b2a_hex(channel_adr).decode(),
                                                                                                                                                   b2a_hex(channel['market']).decode(),
                                                                                                                                                   b2a_hex(channel['delegate']).decode(),
                                                                                                                                                   cstate,
                                                                                                                                                   amount,
                                                                                                                                                   remaining))

        self.log.info('-' * 120)

        self.leave()

    def onLeave(self, details):
        self.log.debug('{klass}.onLeave(details.reason="{reason}", details.message="{message}")',
                       klass=self.__class__.__name__, reason=details.reason, message=details.message if details.message else '')
        runner = self.config.extra.get('runner', None)
        if runner:
            try:
                runner.stop()
            except:
                self.log.failure()
        self.disconnect()

    def onDisconnect(self):
        from twisted.internet import reactor
        try:
            reactor.stop()
        except:
            pass


def main(w3, accounts, owner, markets, args):
    market_id = a2b_hex(markets[0]['id'][2:])

    # 1) show test accounts
    #
    print('-' * 120)
    print('Test accounts:')
    for ak in accounts:
        acct = accounts[ak]
        balance_eth = w3.eth.getBalance(acct.address)
        balance_xbr = xbr.xbrtoken.functions.balanceOf(acct.address).call()

        # the XBR token has 18 decimal digits
        balance_xbr = int(balance_xbr / 10 ** 18)
        print('    balances of {} {:>25}: {:>30} ETH {:>30} XBR'.format(acct.address, ak, balance_eth, balance_xbr))

    print('-' * 120)
    print('Channels in market (on-chain information):')
    channels = []
    for market in markets:
        market_id = market['id']
        for actor in market['actors']:
            actor_adr = actor['addr']
            channels.extend(xbr.xbrnetwork.functions.getAllPaymentChannels(market_id, actor_adr).call())
            channels.extend(xbr.xbrnetwork.functions.getAllPayingChannels(market_id, actor_adr).call())

    channels_ = []
    for channel_adr in channels:
        if type(channel_adr) == tuple:
            continue
        channel = w3.eth.contract(address=channel_adr, abi=xbr.XBR_CHANNEL_ABI).functions
        if channel:
            amount = int(channel.amount().call() / 10**18)
            ctype = channel.ctype().call()
            cstate = channel.state().call()
            balance = int(xbr.xbrtoken.functions.balanceOf(channel_adr).call() / 10**18)

            if ctype in [1, 2]:
                channels_.append((channel_adr, ctype, cstate))
            else:
                print('Skipping unknown channel type {} for address {}'.format(ctype, channel_adr))

            ctype = {0: 'No Channel', 1: 'Payment Channel', 2: 'Paying Channel'}.get(ctype, 'UNKNOWN')
            cstate = {0: None, 1: 'OPEN', 2: 'CLOSING', 3: 'CLOSED', 4: 'FAILED'}.get(cstate, 'UNKNOWN')

            print('    {:<16} {}: currently in {} state, initial amount {} XBR, current on-chain balance {} XBR'.format(ctype, channel_adr, cstate, amount, balance))
            if False:
                print('channel:',
                      channel_adr, channel.channelType().call(), channel.channelState().call(), channel.marketId().call(),
                      channel.sender().call(), channel.delegate().call(), channel.recipient().call(), channel.amount().call(),
                      channel.openedAt().call(), channel.closedAt().call(), channel.channelTimeout().call())

    # now actually run a WAMP client using our session class ClientSession
    extra = {
        'runner': None,
        'channels': channels_,
    }
    runner = ApplicationRunner(url=args.url, realm=args.realm, extra=extra)
    extra['runner'] = runner
    runner.run(MarketMakerClient, auto_reconnect=True)


if __name__ == '__main__':
    print('Using web3.py v{}'.format(web3.__version__))

    parser = argparse.ArgumentParser()

    parser.add_argument('-d',
                        '--debug',
                        action='store_true',
                        help='Enable debug output.')

    parser.add_argument('--gateway',
                        dest='gateway',
                        type=str,
                        default=None,
                        help='Ethereum HTTP gateway URL or None for auto-select (default: -, means let web3 auto-select).')

    parser.add_argument('--url',
                        dest='url',
                        type=six.text_type,
                        default=os.environ.get('CBURL', u'ws://localhost:8080/ws'),
                        help='The router URL (default: "ws://localhost:8080/ws").')

    parser.add_argument('--realm',
                        dest='realm',
                        type=six.text_type,
                        default=os.environ.get('CBREALM', u'realm1'),
                        help='The realm to join (default: "realm1").')

    args = parser.parse_args()

    # start logging
    if args.debug:
        txaio.start_logging(level='debug')
    else:
        txaio.start_logging(level='info')

    if args.gateway:
        w3 = web3.Web3(web3.Web3.HTTPProvider(args.gateway))
    else:
        # using automatic provider detection:
        from web3.auto import w3

    # check we are connected, and check network ID
    if not w3.isConnected():
        print('Could not connect to Web3/Ethereum at: {}'.format(args.gateway or 'auto'))
        sys.exit(1)
    else:
        print('Connected to provider "{}"'.format(args.gateway or 'auto'))
    # set new provider on XBR library
    xbr.setProvider(w3)

    # now enter main ..
    # main(w3.eth.accounts)
    main(w3, ACCOUNTS, OWNER, MARKETS, args)
