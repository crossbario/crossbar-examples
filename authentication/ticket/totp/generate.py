from autobahn.util import utcnow
from autobahn.wamp.auth import generate_totp_secret, compute_totp

TOTP_SEEDS = [
    {'user': 'tobias1', 'seed': 'CACKN3GRF3KQZMEK'},
    {'user': 'user1', 'seed': 'BKIV3FXPRA67N4Q5'}
]

print([compute_totp(s['seed']) for s in TOTP_SEEDS])
