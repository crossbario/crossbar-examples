import sys
import binascii

from init_data import MARKETS

xbrmm_key_file = sys.argv[1]

#from init_data import ACCOUNTS, _ACCOUNT_KEYS
#xbr_marketmaker = 'marketop1-marketmaker1'
#addr, pkey = _ACCOUNT_KEYS[ACCOUNTS[xbr_marketmaker]]

addr = MARKETS[0]['maker']
pkey = MARKETS[0]['maker_pkey']

print(xbrmm_key_file)

with open(xbrmm_key_file, 'wb') as f:
    pkey = binascii.a2b_hex(pkey[2:])
    f.write(pkey)

print('XBR market maker with address 0x{}: private key written to file "{}"'.format(addr, xbrmm_key_file))
