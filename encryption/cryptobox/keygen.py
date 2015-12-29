from nacl.public import PrivateKey
from nacl.encoding import Base64Encoder

key = PrivateKey.generate()
print("PRIVKEY = u'{}'".format(key.encode(encoder=Base64Encoder)))
print("PUBKEY = u'{}'".format(key.public_key.encode(encoder=Base64Encoder)))
