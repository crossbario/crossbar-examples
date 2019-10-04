import sys
import web3

import txaio
txaio.use_twisted()

from autobahn import xbr
import argparse
from init_data import ACCOUNTS, OWNER, MARKETS

# getAllMarketChannels(bytes16 marketId)

def main(accounts, owner, initial_transfer=False):
    print('Using XBR token contract address: {}'.format(xbr.xbrtoken.address))
    print('Using XBR network contract address: {}'.format(xbr.xbrnetwork.address))

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
        print('    balances of {} {:>20}: {:>30} ETH {:>30} XBR'.format(acct.address, ak, balance_eth, balance_xbr))

    # 2) transfer some tokens (every user gets 1m XBR)
    #
    if initial_transfer:
        print('-' * 120)
        # transfer 50,000 XBR
        for ak, amount in [
            ('marketop1', 50000),
            ('marketop1-marketmaker1', 50000),
            ('seller1', 50000),
            ('seller3', 50000),
            ('buyer1', 50000),
            ('buyer3', 50000),
            ('marketop2', 50000),
            ('marketop2-marketmaker1', 50000),
            ('seller2', 50000),
            ('buyer2', 50000),
        ]:
            acct = accounts[ak]
            balance_eth = w3.eth.getBalance(acct.address)
            balance_xbr = xbr.xbrtoken.functions.balanceOf(acct.address).call()

            # the XBR token has 18 decimal digits
            balance_xbr = int(balance_xbr / 10 ** 18)

            print('Balances of {}: {:>30} ETH, {:>30} XBR'.format(acct.address, balance_eth, balance_xbr))

            if balance_xbr < amount:
                transfer_amount = amount - balance_xbr

                # the XBR token has 18 decimal digits
                raw_amount = transfer_amount * 10 ** 18
                success = xbr.xbrtoken.functions.transfer(acct.address, raw_amount).transact({'from': owner.address, 'gas': 100000})
                if success:
                    print('Transferred {} XBR to {}'.format(transfer_amount, acct.address))
                else:
                    print('Failed to transfer tokens!')
            else:
                print('Address {} already has (at least) {} XBR (current balance {} XBR)'.format(acct.address, amount, balance_xbr))

    # 3) register XBR network members
    #
    print('-' * 120)
    for ak in [
        'marketop1',
        'seller1',
        'seller3',
        'buyer1',
        'buyer3',
        'marketop2',
        'seller2',
        'buyer2',
        ]:
        acct = accounts[ak]
        joined, eula, profile, level = xbr.xbrnetwork.functions.members(acct.address).call()
        if not joined:
            eula = 'QmV1eeDextSdUrRUQp9tUXF8SdvVeykaiwYLgrXHHVyULY'
            profile = ''
            xbr.xbrnetwork.functions.register(eula, profile).transact({'from': acct.address, 'gas': 200000})
            print('New member {} address registered in the XBR Network (eula={}, profile={})'.format(acct.address, eula, profile))
        else:
            print('Address {} is already a member (level={}, eula={}, profile={})'.format(acct.address, level, eula, profile))

    # 4) open XBR markets
    #
    print('-' * 120)
    for market in MARKETS:

        _created, _marketSeq, _owner, _terms, _terms, _maker, _providerSecurity, _consumerSecurity, _marketFee = xbr.xbrnetwork.functions.markets(market['id']).call()

        gas = 2000000
        if _created:
            if _owner != market['owner']:
                print('Market {} already exists, but has wrong owner!! Expected {}, but owner is {}'.format(market['id'], market['owner'], _owner))
            else:
                print('Market {} already exists and has expected owner {}'.format(market['id'], _owner))
        else:
            # bytes16 marketId, string memory terms, string memory meta, address maker,
            # uint256 providerSecurity, uint256 consumerSecurity, uint256 marketFee
            providerSecurity = market['providerSecurity'] * 10 ** 18
            consumerSecurity = market['consumerSecurity'] * 10 ** 18

            xbr.xbrnetwork.functions.createMarket(
                market['id'],
                market['terms'],
                market['meta'],
                market['maker'],
                providerSecurity,
                consumerSecurity,
                market['marketFee']).transact({'from': market['owner'], 'gas': gas})

            print('Market {} created with owner {}!'.format(market['id'], market['owner']))

        print('Market actors:')
        for actor in market['actors']:

            joined, security, meta = xbr.xbrnetwork.functions.getMarketActor(market['id'], actor['addr'], actor['type']).call()
            if joined:
                print('   Account {} is already actor (type={}) in the market'.format(actor['addr'], actor['type']))
            else:
                channel_amount = actor['amount']
                if channel_amount:
                    result = xbr.xbrtoken.functions.approve(xbr.xbrnetwork.address, channel_amount).transact({'from': actor['addr'], 'gas': gas})
                    print('   Approved market security amount {})'.format(int(channel_amount / 10 ** 18)))
                    if not result:
                        print('   Failed to allow transfer of {} tokens for market security!\n{}'.format(int(channel_amount / 10 ** 18), result))
                    else:
                        print('   Allowed transfer of {} XBR from {} to {} as security for joining market'.format(int(channel_amount / 10 ** 18), actor['addr'], xbr.xbrnetwork.address))

                security_bytes = xbr.xbrnetwork.functions.joinMarket(market['id'], actor['type'], actor['meta']).transact({'from': actor['addr'], 'gas': gas})
                if security_bytes:
                    security = web3.Web3.toInt(security_bytes)

                    print('   Actor {} joined market {} as actor type {} (meta {}) with security {}!'.format(actor['addr'], market['id'], actor['type'], actor['meta'], security))


if __name__ == '__main__':
    print('Using web3.py v{}'.format(web3.__version__))

    parser = argparse.ArgumentParser()

    parser.add_argument('--gateway',
                        dest='gateway',
                        type=str,
                        default=None,
                        help='Ethereum HTTP gateway URL or None for auto-select (default: -, means let web3 auto-select).')

    args = parser.parse_args()

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
    main(ACCOUNTS, OWNER)
