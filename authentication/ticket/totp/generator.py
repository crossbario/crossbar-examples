from time import sleep
from autobahn.util import utcnow
from autobahn.wamp.auth import generate_totp_secret, compute_totp, qrcode_from_totp

from authenticator import PRINCIPALS_DB

# generate SVGs for the QR codes of the principals
for principal in PRINCIPALS_DB:
    seed = PRINCIPALS_DB[principal][u'seed']
    issuer = u'Crossbar.io'
    qrcode_data = qrcode_from_totp(seed, principal, issuer)
    filename = u'{}.svg'.format(principal)
    with open(filename, 'wb') as f:
        f.write(qrcode_data)
        print('QR Code for principal {} written to {}'.format(principal, filename))

# generate current TOTP values for all principals each 10s
while True:
    print("\n{}".format(utcnow()))
    for principal in PRINCIPALS_DB:
        seed = PRINCIPALS_DB[principal][u'seed']
        print("{}: {}".format(principal, compute_totp(seed)))
    sleep(10)
