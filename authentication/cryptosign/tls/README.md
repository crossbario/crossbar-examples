# WAMP-cryptosign over TLS authentication

*Last tested: 2020/08/18 using Crossbar.io v20.8.2*

-----

WAMP-cryptosign over TLS authentication example.

In a first terminal, start a [Crossbar.io node](.crossbar/config.json) with a TLS transport listening
on port 8080, and using a [self-signed certificate](.crossbar/client.crt):

```console
make crossbar
```

In a second terminal, start the clients

```console
make clients
```

This will run the following clients in series:

* **Twisted** example over TLS, but *without TLS channel binding*: [python client_tx.py](client_tx.py)
* **Twisted** example over TLS and *with "tls-unique" TLS channel binding*: [python client_tx.py --channel_binding="tls-unique"](client_tx.py)
* **asyncio** example over TLS, but *without TLS channel binding*: [python client_aio.py](client_aio.py)
* **asyncio** example over TLS and *with "tls-unique" TLS channel binding*: [python client_aio.py --channel_binding="tls-unique"](client_aio.py)

```console
(cpy382_1) oberstet@intel-nuci7:~/scm/crossbario/crossbar-examples/authentication/cryptosign/tls$ make clients
python client_tx.py --url wss://localhost:8080 --key .keys/client01.key

2020-08-18T18:53:56+0200 Connecting to wss://localhost:8080: requesting realm=None, authid=None
2020-08-18T18:53:56+0200 TLS client using explicit trust (2 certificates)
2020-08-18T18:53:56+0200 TLS client trust root CA certificate loaded from '/home/oberstet/scm/crossbario/crossbar-examples/authentication/cryptosign/tls/.crossbar/intermediate.cert.pem'
2020-08-18T18:53:56+0200 TLS client trust root CA certificate loaded from '/home/oberstet/scm/crossbario/crossbar-examples/authentication/cryptosign/tls/.crossbar/ca.cert.pem'
2020-08-18T18:53:56+0200 initializing component: ComponentConfig(realm=<None>, extra={'channel_binding': None, 'authid': None, 'key': '.keys/client01.key'}, keyring=None, controller=None, shared=None, runner=<autobahn.twisted.wamp.ApplicationRunner object at 0x7f761bbbd670>)
2020-08-18T18:53:56+0200 client public key loaded: 545efb0a2192db8d43f118e9bf9aee081466e1ef36c708b96ee6f62dddad9122
2020-08-18T18:53:56+0200 connected to router
2020-08-18T18:53:56+0200 authenticating using authextra={'pubkey': '545efb0a2192db8d43f118e9bf9aee081466e1ef36c708b96ee6f62dddad9122', 'channel_binding': None} ..
2020-08-18T18:53:56+0200 authentication challenge received: Challenge(method=cryptosign, extra={'challenge': '5f35962096a5e97611c92b8f533b46e3b9a9a1be229de873d637cc9cbd972384', 'channel_binding': None})
2020-08-18T18:53:56+0200 session joined:
SessionDetails(realm="devices",
               session=6842364109815795,
               authid="client01@example.com",
               authrole="device",
               authmethod="cryptosign",
               authprovider="static",
               authextra={'x_cb_node': 'intel-nuci7-323', 'x_cb_worker': 'worker001', 'x_cb_peer': 'tcp4:127.0.0.1:39346', 'x_cb_pid': 337},
               serializer="cbor.batched",
               transport="websocket",
               resumed=None,
               resumable=None,
               resume_token=None)
2020-08-18T18:53:56+0200 ********************************************************************************
2020-08-18T18:53:56+0200 OK, successfully authenticated with WAMP-cryptosign: realm="devices", authid="client01@example.com", authrole="device"
2020-08-18T18:53:56+0200 ********************************************************************************
2020-08-18T18:53:56+0200 session closed: CloseDetails(reason=<wamp.close.normal>, message='None')
2020-08-18T18:53:56+0200 connection to router closed
2020-08-18T18:53:56+0200 Main loop terminated.
python client_tx.py --url wss://localhost:8080 --key .keys/client01.key --channel_binding="tls-unique"

2020-08-18T18:53:56+0200 Connecting to wss://localhost:8080: requesting realm=None, authid=None
2020-08-18T18:53:56+0200 TLS client using explicit trust (2 certificates)
2020-08-18T18:53:56+0200 TLS client trust root CA certificate loaded from '/home/oberstet/scm/crossbario/crossbar-examples/authentication/cryptosign/tls/.crossbar/intermediate.cert.pem'
2020-08-18T18:53:56+0200 TLS client trust root CA certificate loaded from '/home/oberstet/scm/crossbario/crossbar-examples/authentication/cryptosign/tls/.crossbar/ca.cert.pem'
2020-08-18T18:53:57+0200 initializing component: ComponentConfig(realm=<None>, extra={'channel_binding': 'tls-unique', 'authid': None, 'key': '.keys/client01.key'}, keyring=None, controller=None, shared=None, runner=<autobahn.twisted.wamp.ApplicationRunner object at 0x7f1c7c16b760>)
2020-08-18T18:53:57+0200 client public key loaded: 545efb0a2192db8d43f118e9bf9aee081466e1ef36c708b96ee6f62dddad9122
2020-08-18T18:53:57+0200 connected to router
2020-08-18T18:53:57+0200 authenticating using authextra={'pubkey': '545efb0a2192db8d43f118e9bf9aee081466e1ef36c708b96ee6f62dddad9122', 'channel_binding': 'tls-unique'} ..
2020-08-18T18:53:57+0200 authentication challenge received: Challenge(method=cryptosign, extra={'challenge': '0e4b9543f31fbfa02cd9239caf98023edbbe54d4257df888bcbc753a2ea3ac9e', 'channel_binding': 'tls-unique'})
2020-08-18T18:53:57+0200 session joined:
SessionDetails(realm="devices",
               session=3020589441961526,
               authid="client01@example.com",
               authrole="device",
               authmethod="cryptosign",
               authprovider="static",
               authextra={'x_cb_node': 'intel-nuci7-323', 'x_cb_worker': 'worker001', 'x_cb_peer': 'tcp4:127.0.0.1:39352', 'x_cb_pid': 337},
               serializer="cbor.batched",
               transport="websocket",
               resumed=None,
               resumable=None,
               resume_token=None)
2020-08-18T18:53:57+0200 ********************************************************************************
2020-08-18T18:53:57+0200 OK, successfully authenticated with WAMP-cryptosign: realm="devices", authid="client01@example.com", authrole="device"
2020-08-18T18:53:57+0200 ********************************************************************************
2020-08-18T18:53:57+0200 session closed: CloseDetails(reason=<wamp.close.normal>, message='None')
2020-08-18T18:53:57+0200 connection to router closed
2020-08-18T18:53:57+0200 Main loop terminated.
FIXME: client_aio_cnlbind_none
# python client_aio.py --url wss://localhost:8080 --key .keys/client01.key
FIXME: client_aio_cnlbind_unique
# python client_aio.py --url wss://localhost:8080 --key .keys/client01.key --channel_binding="tls-unique"
(cpy382_1) oberstet@intel-nuci7:~/scm/crossbario/crossbar-examples/authentication/cryptosign/tls$
```
