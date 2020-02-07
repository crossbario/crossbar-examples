import sys
import web3

import txaio
txaio.use_twisted()

from autobahn import xbr
import argparse
from binascii import b2a_hex

from init_data import ACCOUNTS, OWNER, MARKETS


def main(accounts, owner):
    # show test accounts
    #
    print('-' * 120)
    print('Test accounts:')
    for ak in accounts:
        acct = accounts[ak]
        balance_eth = w3.eth.getBalance(acct.address)
        balance_xbr = xbr.xbrtoken.functions.balanceOf(acct.address).call()
        balance_xbr = int(balance_xbr / 10 ** 18)
        print('    balances of {} {:>20}: {:>30} ETH {:>30} XBR'.format(acct.address, ak, balance_eth, balance_xbr))

    # open payment channels for (buyer) delegates in markets
    #
    print('-' * 120)
    for market in MARKETS:
        _created, _marketSeq, _owner, _terms, _terms, _maker, _providerSecurity, _consumerSecurity, _marketFee = xbr.xbrnetwork.functions.markets(market['id']).call()

        # assert _owner != '0x0000000000000000000000000000000000000000' and _owner == market['owner']

        print('Market actors:')
        for actor in market['actors']:
            joined, security, meta = xbr.xbrnetwork.functions.getMarketActor(market['id'], actor['addr'], actor['type']).call()
            assert joined

            for delegate in actor['delegates']:
                if actor['type'] == 2:
                    # print('      BUYER-DELEGATE', delegate)

                    for i in range(3):
                        amount = actor['amount']
                        human_amount = int(amount / 10 ** 18)
                        #recipient = actor['addr']
                        #recipient = market['maker']
                        recipient = market['owner']
                        timeout = 60
                        gas = 10000000

                        print('Approving transfer of {} XBR to open channel for recipient {}'.format(human_amount, recipient))

                        result = xbr.xbrtoken.functions.approve(xbr.xbrnetwork.address, amount).transact({'from': actor['addr'], 'gas': gas})
                        if not result:
                            print('Failed to allow transfer of {} XBR token for payment channel!'.format(human_amount, result))
                        else:
                            print('Allowed transfer of {} XBR from {} to {} for opening a payment channel'.format(human_amount, actor['addr'], xbr.xbrnetwork.address))

                            # openPaymentChannel(bytes16 marketId, address delegate, uint256 amount, uint32 timeout)
                            txn = xbr.xbrnetwork.functions.openPaymentChannel(market['id'], recipient, delegate, amount, timeout).transact({'from': actor['addr'], 'gas': gas})
                            receipt = w3.eth.getTransactionReceipt(txn)

                            # bytes16 marketId, address sender, address delegate, address receiver, address channel

                            # args = xbr.xbrtoken.events.Transfer().processReceipt(receipt)
                            # FIXME: MismatchedABI pops up .. we silence this with errors=web3.logs.DISCARD
                            args = xbr.xbrnetwork.events.ChannelCreated().processReceipt(receipt, errors=web3.logs.DISCARD)
                            if args and args[0]:
                                args = args[0].args

                                marketId = args['marketId']
                                sender = args['sender']
                                delegate = args['delegate']
                                recipient = args['recipient']
                                channel = args['channel']

                                # print('Blockchain transaction succeeded:', b2a_hex(receipt.transactionHash).decode(), receipt.gasUsed)
                                print('Actor {} opened **payment channel** {} in market {} with inital deposit of {}, delegate {} and recipient {}!'.format(actor['addr'], channel, market['id'], human_amount, delegate, recipient))
                            else:
                                print('FAILED TO OPEN PAYMENT CHANNEL!', receipt.transactionHash, receipt.gasUsed, args)

    # show test accounts
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
