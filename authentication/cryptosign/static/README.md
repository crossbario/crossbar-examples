# WAMP-cryptosign Static Authentication

## Intro

WAMP-cryptosign is a WAMP level authentication mechanism that allows WAMP client to authentiate to WAMP routers using Curve25519 based cryptography.

In particular, WAMP-cryptosign uses Ed25519 private signing keys for authentication.

WAMP-cryptosign also allows clients to authenticate the router connecting to, so MITM attackes are mitigated.

A WAMP client needs to have a (private) Ed25519 which is used during authentication in the WAMP opening handshake.

When a client wants to authenticate the WAMP router it is connecting to, the client additionally needs to have a **trustroot** defined, which is a *public* Ed25519 key. The WAMP router will present it's public key plus a trustchain originating in the server public key, and ending in the trustroot presented by the client.

AutobahnPython supports the following sources for such keys:

1. raw binary string (32 bytes): [client_raw_key.py](client_raw_key.py)
2. SSH private key: [client_ssh_key.py](client_ssh_key.py)
3. SSH private key held in SSH agent: [client_ssh_agent.py](client_ssh_agent.py)


## Using WAMP-cryptosign with OpenSSH

OpenSSH can be used to

* generate keys for use with WAMP-cryptosign
* hold private keys in `ssh-agent`

### Generating Ed25519 keys

To generate a new Ed25519 key:

```console
oberstet@corei7ub1310:~$ ssh-keygen -t ed25519
Generating public/private ed25519 key pair.
Enter file in which to save the key (/home/oberstet/.ssh/id_ed25519): 
Enter passphrase (empty for no passphrase): 
Enter same passphrase again: 
Your identification has been saved in /home/oberstet/.ssh/id_ed25519.
Your public key has been saved in /home/oberstet/.ssh/id_ed25519.pub.
The key fingerprint is:
SHA256:Wn0VrI0mMGaBELuq6dqJdRye26D/gqM2UT6B3JtWlQs oberstet@corei7ub1310
The key's randomart image is:
+--[ED25519 256]--+
|    oo .o.   ..  |
|     E.o=     .. |
|. o . oo.o   +.  |
| o + o . .. +..  |
|  o B   S .o.    |
| . X o o   .     |
|  =.B .          |
| Oo+.+           |
|Xo=oooo          |
+----[SHA256]-----+
```

An OpenSSH Ed25519 

### Using Ed25519 with `ssh-agent`

OpenSSH keys held in `ssh-agent` can be used like this:

```python
from autobahn.wamp.cryptosign import SSHAgentSigningKey
...
# create a proxy signing key with the private key being held in SSH agent
key = yield SSHAgentSigningKey.new(pubkey)
```

Here, `pubkey` should be a string with the public key part of the keypair held in `ssh-agent`, e.g.

```
ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIFhd9RmReA7o3OR2YyQFigTsrkKd/9eG7oCDnJRnRowo oberstet@corei7ub1310
```

#### Disable Gnome keyring

Ubuntu 14.04 is using Gnome keyring for managing and holding SSH keys. This app is outdated, and [does not support Ed25519 keys](https://bugs.launchpad.net/ubuntu/+source/gnome-keyring/+bug/1393531).

We'll be using [OpenSSH portable](http://www.openssh.com/portable.html) from [upstream](http://www.openbsd.org/) instead.

First, we need to disable Gnome keyring. There are lots of recipes on the net. The only one that worked for me is this:

```console
sudo chmod -x /usr/bin/gnome-keyring*
sudo chmod -x /usr/bin/ssh-agent
```

Reboot your machine.

#### Build and install OpenSSH portable

Visit [OpenSSH portable download mirrors](http://www.openssh.com/portable.html#mirrors) to get the latest release:

```console
cd /tmp
wget http://openbsd.cs.fau.de/pub/OpenBSD/OpenSSH/portable/openssh-7.1p2.tar.gz
tar xvf openssh-7.1p2.tar.gz
cd openssh-7.1p2
./configure --prefix=/opt/openssh
make
sudo make install
```

This should give you

```
oberstet@corei7ub1310:~$ /opt/openssh/bin/ssh -V
OpenSSH_7.1p2, OpenSSL 1.0.1f 6 Jan 2014
```

#### Autostart SSH agent

Add the following to your `$HOME/.bashrc`:

```shell
export PATH=/opt/openssh/bin:${PATH}

env=~/.ssh/agent.env

agent_is_running() {
    if [ "$SSH_AUTH_SOCK" ]; then
        # ssh-add returns:
        #   0 = agent running, has keys
        #   1 = agent running, no keys
        #   2 = agent not running
        ssh-add -l >/dev/null 2>&1 || [ $? -eq 1 ]
    else
        false
    fi
}

agent_has_keys() {
    ssh-add -l >/dev/null 2>&1
}

agent_load_env() {
    . "$env" >/dev/null
}

agent_start() {
    (umask 077; ssh-agent >"$env")
    . "$env" >/dev/null
}

if ! agent_is_running; then
    agent_load_env
fi

if ! agent_is_running; then
    agent_start
    ssh-add
elif ! agent_has_keys; then
    ssh-add
fi

unset env
```

When SSH agent is running, it'll set a environment variable pointing to the Unix domain socket it is listening on:

```console
oberstet@corei7ub1310:~$ echo $SSH_AUTH_SOCK
/tmp/ssh-nglQGz2LuI7v/agent.13601
```

#### Securing use of `ssh-agent`

For maximum security, the following measures should be taken:

1. run an SSH agent under a dedicated account, different from the one running your WAMP component
2. nobody but that dedicated account should have access to the private keys held (using filesystem permissions)
3. access to the SSH agent's listening Unix domain socket should be restricted to the account running your WAMP components (using filesystem permissions)


## Using WAMP-cryptosign with Putty?

**Autobahn|Python does [not support](https://github.com/crossbario/autobahn-python/issues/577) Putty/Pageant for WAMP-cryptosign**. This section is mainly for noting that, and for users that want to use Ed25519 for general SSH with Putty.

The current *release* of Putty (version 0.66 as of 15.1.2016) does **not** support Ed25519. Only the *development snapshot* does.

Get it [here](http://tartarus.org/~simon/putty-snapshots/x86/putty-installer.exe).


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
           "authorized_keys": [
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
