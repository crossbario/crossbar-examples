from time import sleep
from autobahn.util import utcnow
from autobahn.wamp.auth import generate_totp_secret, compute_totp

from authenticator import PRINCIPALS_DB

while True:
    print("\n{}".format(utcnow()))
    for principal in PRINCIPALS_DB:
        seed = PRINCIPALS_DB[principal][u'seed']
        print("{}: {}".format(principal, compute_totp(seed)))
    sleep(10)
