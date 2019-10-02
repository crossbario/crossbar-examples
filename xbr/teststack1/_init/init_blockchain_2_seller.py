import sys
import web3
import uuid

import txaio
txaio.use_twisted()

from autobahn import xbr
import argparse
from binascii import b2a_hex

from init_data import ACCOUNTS, OWNER, MARKETS


def main(accounts, owner):
    # 1) show test accounts
    #
    print('-' * 120)
    print('Test accounts:')
    for ak in accounts:
        acct = accounts[ak]
        balance_eth = w3.eth.getBalance(acct.address)
        balance_xbr = xbr.xbrtoken.functions.balanceOf(acct.address).call()
        balance_xbr = int(balance_xbr / 10 ** 18)
        print('    balances of {} {:>20}: {:>30} ETH {:>30} XBR'.format(acct.address, ak, balance_eth, balance_xbr))

    # 2) request paying channels for delegates in markets
    #
    print('-' * 120)
    for market in MARKETS:
        _created, _marketSeq, _owner, _terms, _terms, _maker, _providerSecurity, _consumerSecurity, _marketFee = xbr.xbrnetwork.functions.markets(market['id']).call()

        assert _owner != '0x0000000000000000000000000000000000000000' and _owner == market['owner']

        print('Market actors:')
        for actor in market['actors']:
            joined, security, meta = xbr.xbrnetwork.functions.getMarketActor(market['id'], actor['addr'], actor['type']).call()
            assert joined

            for delegate in actor['delegates']:
                if actor['type'] == 1:
                    # print('      SELLER-DELEGATE', delegate)

                    for i in range(3):
                        amount = actor['amount']
                        timeout = 60
                        gas = 1000000

                        # requestPayingChannel(bytes16 marketId, address recipient, address delegate, uint256 amount, uint32 timeout)
                        recipient = actor['addr']
                        txn = xbr.xbrnetwork.functions.requestPayingChannel(market['id'], recipient, delegate, amount, timeout).transact(
                            {'from': actor['addr'], 'gas': gas})
                        receipt = w3.eth.getTransactionReceipt(txn)

                        # PayingChannelRequestCreated(bytes16 marketId, address sender, address recipient, address delegate, uint256 amount, uint32 timeout)
                        # FIXME: MismatchedABI pops up .. we silence this with errors=web3.logs.DISCARD
                        args = xbr.xbrnetwork.events.PayingChannelRequestCreated().processReceipt(receipt, errors=web3.logs.DISCARD)
                        if args and args[0]:
                            args = args[0].args

                            marketId = args['marketId']
                            sender = args['sender']
                            recipient = args['recipient']
                            delegate = args['delegate']
                            amount = args['amount']
                            timeout = args['timeout']

                            # print('Blockchain transaction succeeded:', b2a_hex(receipt.transactionHash).decode(), receipt.gasUsed)
                            print('Actor {} requested paying channel in market {} with amount {} XBR, delegate {} and recipient {}!'.format(
                                actor['addr'], uuid.UUID(bytes=marketId), amount, delegate, recipient))
                        else:
                            print('FAILED TO OPEN PAYING CHANNEL!', receipt.transactionHash, receipt.gasUsed, args)

    # 3) show test accounts
    #
    print('-' * 120)
    print('Test accounts:')
    for ak in accounts:
        acct = accounts[ak]
        balance_eth = w3.eth.getBalance(acct.address)
        balance_xbr = xbr.xbrtoken.functions.balanceOf(acct.address).call()
        balance_xbr = int(balance_xbr / 10 ** 18)
        print('    balances of {} {:>20}: {:>30} ETH {:>30} XBR'.format(acct.address, ak, balance_eth, balance_xbr))


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
