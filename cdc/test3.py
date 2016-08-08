import os
from autobahn.wamp import cryptosign

fn = os.path.join(os.path.expanduser('~'), '.ssh', 'id_ed25519')
fn = 'oberstet'

key = cryptosign.SigningKey.from_ssh_key(fn)
print(key.public_key())
print(key.comment())
print(key.can_sign())
