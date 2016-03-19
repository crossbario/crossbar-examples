# WAMP-cryptosign Dynamic Authentication

This example shows how to authenticate WAMP clients using WAMP-cryptosign as the authentication method, and using a dynamic authenticator to actually lookup and authenticate clients.

While Crossbar.io is doing all the heavy lifting of managing the WAMP-cryptosign authentication handshake, user code (the dynamic authenticator) can hook into authentication at a central place.

For example, user code could lookup clients in a persistent database, such as a key-value store or a relational database.

## How to run

For the impatient:

```console
make crossbar
make client
make bad_client
```

In a first terminal, start Crossbar.io:

    crossbar start

This should give you

```console
(python279_1)oberstet@thinkpad-t430s:~/scm/crossbario/crossbarexamples/authentication/cryptosign/dynamic$ crossbar start
2016-03-19T22:35:54+0100 [Controller  20161] Automatically choosing optimal Twisted reactor
2016-03-19T22:35:54+0100 [Controller  20161] Running on Linux and optimal reactor (epoll) was installed.
2016-03-19T22:35:55+0100 [Controller  20161]      __  __  __  __  __  __      __     __
2016-03-19T22:35:55+0100 [Controller  20161]     /  `|__)/  \/__`/__`|__) /\ |__)  |/  \
2016-03-19T22:35:55+0100 [Controller  20161]     \__,|  \\__/.__/.__/|__)/~~\|  \. |\__/
2016-03-19T22:35:55+0100 [Controller  20161]
2016-03-19T22:35:55+0100 [Controller  20161]     Crossbar.io Version: 0.13.0
2016-03-19T22:35:55+0100 [Controller  20161]     Node Public Key: 63f1cad6c7a35cbb3fdf559a35e89b47e29589457522e37d79aaad9a307608f0
2016-03-19T22:35:55+0100 [Controller  20161]
2016-03-19T22:35:55+0100 [Controller  20161] Running from node directory '/home/oberstet/scm/crossbario/crossbarexamples/authentication/cryptosign/dynamic/.crossbar'
2016-03-19T22:35:55+0100 [Controller  20161] Controller process starting (CPython-EPollReactor) ..
2016-03-19T22:35:55+0100 [Controller  20161] Node configuration loaded from 'config.json'
2016-03-19T22:35:55+0100 [Controller  20161] Node ID 'thinkpad-t430s' set from hostname
2016-03-19T22:35:55+0100 [Controller  20161] Using default node shutdown triggers [u'shutdown_on_worker_exit']
2016-03-19T22:35:55+0100 [Controller  20161] Joined realm 'crossbar' on node management router
2016-03-19T22:35:55+0100 [Controller  20161] Starting Router with ID 'worker1'...
2016-03-19T22:35:55+0100 [Router      20166] Worker process starting (CPython-EPollReactor) ..
2016-03-19T22:35:56+0100 [Controller  20161] Router with ID 'worker1' and PID 20166 started
2016-03-19T22:35:56+0100 [Router      20166] Realm 'realm-auth' started
2016-03-19T22:35:56+0100 [Controller  20161] Router 'worker1': realm 'realm1' (named 'realm-auth') started
2016-03-19T22:35:56+0100 [Controller  20161] Router 'worker1': role 'role1' (named 'authenticator') started on realm 'realm1'
2016-03-19T22:35:56+0100 [Router      20166] Realm 'devices' started
2016-03-19T22:35:56+0100 [Controller  20161] Router 'worker1': realm 'realm2' (named 'devices') started
2016-03-19T22:35:56+0100 [Controller  20161] Router 'worker1': role 'role1' (named 'device') started on realm 'realm2'
2016-03-19T22:35:56+0100 [Router      20166] started component: authenticator.AuthenticatorSession id=3544877339570676
2016-03-19T22:35:56+0100 [Router      20166] Dynamic authenticator registered!
2016-03-19T22:35:56+0100 [Controller  20161] Router 'worker1': component 'component1' started
2016-03-19T22:35:56+0100 [Router      20166] WampWebSocketServerFactory starting on 8080
2016-03-19T22:35:56+0100 [Controller  20161] Router 'worker1': transport 'transport1' started
...
```

In a second terminal, start the example client that connects to Crossbar.io:

    python client.py --key client01.key

This should give you

```console
(python279_1)oberstet@thinkpad-t430s:~/scm/crossbario/crossbarexamples/authentication/cryptosign/dynamic$ python client.py --key client01.key
2016-03-19T22:36:55+0100 Connecting to ws://localhost:8080/ws: realm=None, authid=None
2016-03-19T22:36:55+0100 initializing component: ComponentConfig(realm=<None>, extra={u'key': u'client01.key', u'authid': None}, keyring=None)
2016-03-19T22:36:55+0100 client public key loaded: 545efb0a2192db8d43f118e9bf9aee081466e1ef36c708b96ee6f62dddad9122
2016-03-19T22:36:55+0100 connected to router
2016-03-19T22:36:55+0100 authentication challenge received: Challenge(method=cryptosign, extra={u'challenge': '07250e55ec667085a467ddb2bc701bd6a4632d0245e4a05464993195f59801a5'})
2016-03-19T22:36:55+0100 session joined: SessionDetails(realm=<devices>, session=5168110867993443, authid=<client01@example.com>, authrole=<device>, authmethod=cryptosign, authprovider=dynamic, authextra={'foo': 23L})
2016-03-19T22:36:55+0100 *** Hooray! We've been successfully authenticated with WAMP-cryptosign using Ed25519! ***
2016-03-19T22:36:55+0100 session closed: CloseDetails(reason=<wamp.close.normal>, message='None')
2016-03-19T22:36:55+0100 connection to router closed
2016-03-19T22:36:55+0100 Main loop terminated.
```

The client has successfully authenticated.

More so, it was authenticated:

* `realm = "devices"`
* `authid = "client01@example.com"`
* `authrole = "device"`

and with `authextra` information `{'foo': 23L}`.

When looking at the output from the dynamic authenticator which was captured and printed to the first terminal, you should get:

```console
2016-03-19T22:42:10+0100 [Router      20234] WAMP-cryptosign CHANNEL BINDING requested: tls-unique
2016-03-19T22:42:10+0100 [Router      20234] authenticating session with public key = 545efb0a2192db8d43f118e9bf9aee081466e1ef36c708b96ee6f62dddad9122
2016-03-19T22:42:10+0100 [Router      20234] found valid principal client01@example.com matching public key
```
