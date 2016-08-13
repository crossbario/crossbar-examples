import os
import binascii
from asyncssh.packet import SSHPacket
from nacl import bindings

from asyncssh.public_key import _decode_openssh_private

_OPENSSH_KEY_V1 = b'openssh-key-v1\0'

# https://github.com/ronf/asyncssh/blob/master/asyncssh/public_key.py
# https://github.com/ronf/asyncssh/blob/master/asyncssh/ed25519.py
# http://cvsweb.openbsd.org/cgi-bin/cvsweb/src/usr.bin/ssh/PROTOCOL.key

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

        blob = blob[len(_OPENSSH_KEY_V1):]
        packet = SSHPacket(blob)

        cipher_name = packet.get_string()
        kdf = packet.get_string()
        kdf_data = packet.get_string()
        nkeys = packet.get_uint32()
        _ = packet.get_string()                 # public_key
        key_data = packet.get_string()
        mac = packet.get_remaining_payload()

        block_size = 8

        if cipher_name != b'none':
            raise Exception('encrypted private keys not supported (please remove the passphrase from your private key or use SSH agent)')

        if kdf != b'none':
            raise Exception('passphrase encrypted private keys not supported')

        if nkeys != 1:
            raise Exception('multiple private keys in a key file not supported (found {} keys)'.format(nkeys))

        if mac:
            raise Exception('invalid OpenSSH private key (found remaining payload for mac)')

        print('cipher_name', cipher_name)
        print('kdf', kdf)
        print('kdf_data', kdf_data)
        print('nkeys', nkeys)
        print('key_data', key_data)
        print('mac', mac)

        packet = SSHPacket(key_data)
        check1 = packet.get_uint32()
        check2 = packet.get_uint32()
        alg = packet.get_string()

        if alg != b'ssh-ed25519':
            raise Exception('invalid key type: we only support Ed25519 (found "{}")'.format(alg.decode('ascii')))

        print('alg', alg)

        vk = packet.get_string()
        sk = packet.get_string()

        if len(vk) != bindings.crypto_sign_PUBLICKEYBYTES:
            raise Exception('invalid public key length')

        if len(sk) != bindings.crypto_sign_SECRETKEYBYTES:
            raise Exception('invalid public key length')

        comment = packet.get_string()                             # comment
        pad = packet.get_remaining_payload()

        if len(pad) >= block_size or pad != bytes(range(1, len(pad) + 1)):
            raise Exception('invalid OpenSSH private key')

        # secret key (64 octets) = 32 octets seed || 32 octets secret key derived of seed
        # crypto_sign_ed25519_sk_to_seed
        # https://github.com/jedisct1/libsodium/blob/master/src/libsodium/crypto_sign/ed25519/sign_ed25519_api.c#L27

        print(binascii.b2a_hex(sk))

        seed = sk[:bindings.crypto_sign_SEEDBYTES]
        print(binascii.b2a_hex(seed))

        return len(vk), len(sk), comment
    else:
        # SSH public key
        keydata = _read_ssh_ed25519_pubkey(filename)
        key = public.PublicKey(keydata)
        return cls(key)

fn = os.path.join(os.path.expanduser('~'), '.ssh', 'id_ed25519')
fn = 'oberstet'

k = from_ssh_key(fn)
print(k)
