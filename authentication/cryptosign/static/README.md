# WAMP-cryptosign Static Authentication

## How to try

Run Crossbar.io in a first terminal from this directory. Then, in a second terminal, start the client:

```console
(python279_1)oberstet@thinkpad-t430s:~/scm/crossbario/crossbarexamples/authentication/cryptosign/static$ python client.py --key client01.key
Connecting to ws://localhost:8080/ws: realm=None, authid=None
2016-01-05T17:54:31+0100 __init__(config=ComponentConfig(realm=<None>, extra={u'key': u'client01.key', u'authid': None}, keyring=None))
2016-01-05T17:54:31+0100 Client public key loaded: 545efb0a2192db8d43f118e9bf9aee081466e1ef36c708b96ee6f62dddad9122
2016-01-05T17:54:31+0100 onConnect()
2016-01-05T17:54:31+0100 onChallenge(challenge=Challenge(method=cryptosign, extra={u'challenge': '800e870c77bfa62fbe17305f262ea6595532f09fcb54550b39648fc5255609af'}))
2016-01-05T17:54:31+0100 onJoin(details=SessionDetails(realm=<devices>, session=3983743498134005, authid=<client01@example.com>, authrole=<device>, authmethod=cryptosign, authprovider=static, authextra=None))
2016-01-05T17:54:31+0100 onLeave(details=CloseDetails(reason=<wamp.close.normal>, message='None'))
2016-01-05T17:54:31+0100 onDisconnect()
2016-01-05T17:54:31+0100 Main loop terminated.
```

## Todo

### Router Authentication

### SSH agent integration

### Authorized keys

```json
"auth": {
  "cryptosign": {
     "type": "static",
     "principals": {
        "client01@example.com": {
           "realm": "devices",
           "role": "device",
           "authorized-keys": [
               "545efb0a2192db8d43f118e9bf9aee081466e1ef36c708b96ee6f62dddad9122",
               "e5b0d24af05c77d644de885946147aeb4fa6897a5cf4eb14347c3d637664b117"
           ]
        }
     }
  }
}
```

**Generating keys for SSH**


Generate a new public-private key pair of type Ed25519, no passphrase and with comment being set to an identifier for your client component:

```console
(python279_1)oberstet@thinkpad-t430s:~/scm/crossbario/crossbarexamples/authentication/cryptosign/static$ ssh-keygen -t ed25519 -N '' -C "client02@example.com" -f client02
Generating public/private ed25519 key pair.
Your identification has been saved in client02.
Your public key has been saved in client02.pub.
The key fingerprint is:
44:f7:8d:f4:60:94:48:3f:0c:c7:d7:db:f0:bf:46:35 client02@example.com
The key's randomart image is:
+--[ED25519  256--+
|        ..++*. . |
|       . ..Oo=o .|
|        .   *.ooo|
|       .     . E+|
|        S       +|
|               ..|
|              . .|
|               o |
|              .  |
+-----------------+
```

The client public key part is stored in `client02.pub`

```console
(python279_1)oberstet@thinkpad-t430s:~/scm/crossbario/crossbarexamples/authentication/cryptosign/static$ cat client02.pub
ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIOWw0krwXHfWRN6IWUYUeutPpol6XPTrFDR8PWN2ZLEX client02@example.com
```
