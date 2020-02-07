from eth_account import Account
from autobahn import xbr

from autobahn.xbr import account_from_seedphrase

__all__ = ('ACCOUNTS', 'OWNER', 'MARKETS')


if 'XBR_HDWALLET_SEED' not in os.environ:
    raise RuntimeError('XBR_HDWALLET_SEED not set!')
_XBR_HDWALLET_SEED = os.environ['XBR_HDWALLET_SEED']


_ACCOUNT_KEYS = {}
for i in range(20):
    acct = account_from_seedphrase(_XBR_HDWALLET_SEED)
    addr = acct.address
    pkey = acct.privateKey.hex()
    _ACCOUNT_KEYS[i] = (addr, pkey)


_INITDATA = [
    (0,  'crossbar',                'XBR Smart Contracts Developers (deployer and owner).'),
    (1,  'seller1',                 'Example XBR Seller (service provider).'),
    (2,  'buyer1',                  'Example XBR Buyer (service consumer).'),
    (3,  'marketop1',               'Example XBR Market (marketplace operator).'),
    (4,  'seller1-delegate1',       'XBR Python-based Seller 1 Delegate 1'),
    (5,  'buyer1-delegate1',        'XBR Python-based Buyer 1 Delegate 1'),
    (6,  'marketop1-marketmaker1',  'XBR Market Maker 1 (of marketop1)'),
    (7,  'seller1-delegate2',       'XBR NodeJS-based Seller 1 Delegate 2'),
    (8,  'buyer1-delegate2',        'XBR NodeJS-based Buyer 1 Delegate 2'),
    (9,  'marketop2',               'Example XBR Market (marketplace operator).'),
    (10, 'marketop2-marketmaker1',  'XBR Market Maker 1 (of marketop2)'),
    (11, 'seller2',                 'Example XBR Seller (service provider).'),
    (12, 'buyer2',                  'Example XBR Buyer (service consumer).'),
    (13, 'seller2-delegate1',       'XBR Browser-based Seller Delegate 1 (of seller2)'),
    (14, 'buyer2-delegate1',        'XBR Browser-based Buyer Delegate 1 (of buyer2)'),
    (15, 'seller3',                 'Example XBR Seller (service provider).'),
    (16, 'buyer3',                  'Example XBR Buyer (service consumer).'),
    (17, 'seller3-delegate1',       'XBR Seller Delegate 3 (of seller1)'),
    (18, 'buyer3-delegate1',        'XBR Buyer Delegate 3 (of buyer1)'),
]

ACCOUNTS = {}
for idx, name, notes in _INITDATA:
    (addr, pkey) = _ACCOUNT_KEYS[idx]
    ACCOUNTS[name] = Account.privateKeyToAccount(pkey)

OWNER = ACCOUNTS['crossbar']

MARKETS = [
    {
        'id': '0xa1b8d6741ae8492017fafd8d4f8b67a2',
        'owner': ACCOUNTS['marketop1'].address,
        'maker': ACCOUNTS['marketop1-marketmaker1'].address,
        'terms': '',
        'meta': '',
        'providerSecurity': 0,
        'consumerSecurity': 0,
        'marketFee': 0,
        'actors': [
            # seller 1
            {
                'addr': ACCOUNTS['seller1'].address,
                'type': 1,
                'meta': '',
                'amount': 1000 * 10 ** 18,
                'delegates': [
                    # ABPy seller
                    ACCOUNTS['seller1-delegate1'].address,

                    # ABJS NodeJS seller
                    ACCOUNTS['seller1-delegate2'].address,
                ]
            },
            # buyer 1
            {
                'addr': ACCOUNTS['buyer1'].address,
                'type': 2,
                'meta': '',
                'amount': 500 * 10 ** 18,
                'delegates': [
                    # ABPy buyer
                    ACCOUNTS['buyer1-delegate1'].address,

                    # ABJS NodeJS buyer
                    ACCOUNTS['buyer1-delegate2'].address,
                ]
            },
            # seller 2
            {
                'addr': ACCOUNTS['seller2'].address,
                'type': 1,
                'meta': '',
                'amount': 1000 * 10 ** 18,
                'delegates': [
                    # ABJS Browser seller
                    ACCOUNTS['seller2-delegate1'].address,
                ]
            },
            # buyer 2
            {
                'addr': ACCOUNTS['buyer2'].address,
                'type': 2,
                'meta': '',
                'amount': 500 * 10 ** 18,
                'delegates': [
                    # ABJS Browser buyer
                    ACCOUNTS['buyer2-delegate1'].address,
                ]
            },
            # seller 3
            {
                'addr': ACCOUNTS['seller3'].address,
                'type': 1,
                'meta': '',
                'amount': 1000 * 10 ** 18,
                'delegates': [
                    ACCOUNTS['seller3-delegate1'].address,
                ]
            },
            # buyer 3
            {
                'addr': ACCOUNTS['buyer3'].address,
                'type': 2,
                'meta': '',
                'amount': 500 * 10 ** 18,
                'delegates': [
                    ACCOUNTS['buyer3-delegate1'].address,
                ]
            },
        ]
    },
    # {
    #     'id': '0x4e0ae926edbecce1d983bea725f749df',
    #     'owner': ACCOUNTS['marketop2'].address,
    #     'maker': ACCOUNTS['marketop2-marketmaker1'].address,
    #     'terms': '',
    #     'meta': '',
    #     'providerSecurity': 0,
    #     'consumerSecurity': 0,
    #     'marketFee': 0,
    #     'actors': [
    #         {
    #             'addr': ACCOUNTS['seller2'].address,
    #             'type': 1,
    #             'meta': '',
    #             'amount': 1000 * 10 ** 18,
    #             'delegates': [
    #                 ACCOUNTS['seller2-delegate1'].address,
    #             ]
    #         },
    #         {
    #             'addr': ACCOUNTS['buyer2'].address,
    #             'type': 2,
    #             'meta': '',
    #             'amount': 500 * 10 ** 18,
    #             'delegates': [
    #                 ACCOUNTS['buyer2-delegate1'].address,
    #             ]
    #         },
    #     ]
    # },
]
