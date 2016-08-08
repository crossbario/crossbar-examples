import os
import binascii

import sys, string, base64
from pyasn1.type import univ, namedtype, namedval, constraint
from pyasn1.codec.der import encoder, decoder

class DSAPrivateKey(univ.Sequence):
    """PKIX compliant DSA private key structure"""
    componentType = namedtype.NamedTypes(
        namedtype.NamedType('version', univ.Integer(namedValues=namedval.NamedValues(('v1', 0)))),
        namedtype.NamedType('p', univ.Integer()),
        namedtype.NamedType('q', univ.Integer()),
        namedtype.NamedType('g', univ.Integer()),
        namedtype.NamedType('public', univ.Integer()),
        namedtype.NamedType('private', univ.Integer())
        )

MAX = 16

class OtherPrimeInfo(univ.Sequence):
    componentType = namedtype.NamedTypes(
        namedtype.NamedType('prime', univ.Integer()),
        namedtype.NamedType('exponent', univ.Integer()),
        namedtype.NamedType('coefficient', univ.Integer())
        )

class OtherPrimeInfos(univ.SequenceOf):
    componentType = OtherPrimeInfo()
    subtypeSpec = univ.SequenceOf.subtypeSpec + \
                  constraint.ValueSizeConstraint(1, MAX)

class RSAPrivateKey(univ.Sequence):
    """PKCS#1 compliant RSA private key structure"""
    componentType = namedtype.NamedTypes(
        namedtype.NamedType('version', univ.Integer(namedValues=namedval.NamedValues(('two-prime', 0), ('multi', 1)))),
        namedtype.NamedType('modulus', univ.Integer()),
        namedtype.NamedType('publicExponent', univ.Integer()),
        namedtype.NamedType('privateExponent', univ.Integer()),
        namedtype.NamedType('prime1', univ.Integer()),
        namedtype.NamedType('prime2', univ.Integer()),
        namedtype.NamedType('exponent1', univ.Integer()),
        namedtype.NamedType('exponent2', univ.Integer()),
        namedtype.NamedType('coefficient', univ.Integer()),
        namedtype.OptionalNamedType('otherPrimeInfos', OtherPrimeInfos())
        )

class ECDSAPrivateKey(univ.Sequence):
    """PKCS#1 compliant RSA private key structure"""
    componentType = namedtype.NamedTypes(
        namedtype.NamedType('version', univ.Integer(namedValues=namedval.NamedValues(('two-prime', 0), ('multi', 1)))),
        namedtype.NamedType('key', univ.OctetString()),
        )


def from_ssh_key(filename):
    """
    Load an Ed25519 key from a SSH key file. The key file can be a (private) signing
    key (from a SSH private key file) or a (public) verification key (from a SSH
    public key file). A private key file must be passphrase-less.
    """
    # https://tools.ietf.org/html/draft-bjh21-ssh-ed25519-02
    # http://blog.oddbit.com/2011/05/08/converting-openssh-public-keys/

    SSH_BEGIN = u'-----BEGIN OPENSSH PRIVATE KEY-----'
    SSH_END = u'-----END OPENSSH PRIVATE KEY-----'

    with open(filename, 'r') as f:
        keydata = f.read().strip()

    if keydata.startswith(SSH_BEGIN) and keydata.endswith(SSH_END):
        # SSH private key
        ssh_end = keydata.find(SSH_END)
        keydata = keydata[len(SSH_BEGIN):ssh_end]
        keydata = u''.join([x.strip() for x in keydata.split()])
        print(keydata)
        blob = binascii.a2b_base64(keydata)
        blob = blob[14:]
        print(blob)
        print(len(blob))

        #asn1Spec = ECDSAPrivateKey()

        #key = decoder.decode(blob, asn1Spec=asn1Spec)[0]
        key = decoder.decode(blob)

        print(key.prettyPrint())

        return blob
        # prefix = 'openssh-key-v1\x00'
        # data = unpack(blob[len(prefix):])
        raise Exception("loading private keys not implemented")
    else:
        # SSH public key
        keydata = _read_ssh_ed25519_pubkey(filename)
        key = public.PublicKey(keydata)
        return cls(key)

fn = os.path.join(os.path.expanduser('~'), '.ssh', 'id_ed25519')
fn = 'oberstet'

k = from_ssh_key(fn)
print(k)
