# WAMP-Ed25519 Static Authentication


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
