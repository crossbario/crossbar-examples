# WAMP-cryptosign with dynamic authentication

*Last tested: 2020/08/18 using Crossbar.io v20.8.2*

-----

WAMP-cryptosign with dynamic authentication, using a custom authenticator.

In a first terminal, start a [Crossbar.io node](.crossbar/config.json) with a transport listening
on port 8080, and running a [custom authenticator](authenticator.py):

```console
make crossbar
```

In a second terminal, start the clients

```console
make clients
```

This will run the following client:

* **Twisted** example: [python client.py](client.py)

The client will be run twice, once using a valid key, and once using an invalid key:

```console
(cpy382_1) oberstet@intel-nuci7:~/scm/crossbario/crossbar-examples/authentication/cryptosign/dynamic$ make clients
python client.py --key .keys/client01.key
2020-08-18T16:21:57+0200 Connecting to ws://localhost:8080/ws: requesting realm=None, authid=None
2020-08-18T16:21:57+0200 initializing component: ComponentConfig(realm=<None>, extra={'channel_binding': None, 'authid': None, 'key': '.keys/client01.key'}, keyring=None, controller=None, shared=None, runner=<autobahn.twisted.wamp.ApplicationRunner object at 0x7faff0c6a130>)
2020-08-18T16:21:57+0200 client public key loaded: 545efb0a2192db8d43f118e9bf9aee081466e1ef36c708b96ee6f62dddad9122
2020-08-18T16:21:57+0200 connected to router
2020-08-18T16:21:57+0200 authentication challenge received: Challenge(method=cryptosign, extra={'challenge': 'aebdf4e1c36408d1ed4e5f57358e0b0d3b29513a4884fe0c9ea40bcf6ae1f8fc', 'channel_binding': None})
2020-08-18T16:21:57+0200 session joined:
SessionDetails(realm="devices",
               session=6553397104124258,
               authid="client01@example.com",
               authrole="device",
               authmethod="cryptosign",
               authprovider="dynamic",
               authextra={'foo': 23, 'x_cb_node': 'intel-nuci7-28675', 'x_cb_worker': 'worker001', 'x_cb_peer': 'tcp4:127.0.0.1:38588', 'x_cb_pid': 28685},
               serializer="cbor.batched",
               transport="websocket",
               resumed=None,
               resumable=None,
               resume_token=None)
2020-08-18T16:21:57+0200 ********************************************************************************
2020-08-18T16:21:57+0200 OK, successfully authenticated with WAMP-cryptosign: realm="devices", authid="client01@example.com", authrole="device"
2020-08-18T16:21:57+0200 ********************************************************************************
2020-08-18T16:21:57+0200 session closed: CloseDetails(reason=<wamp.close.normal>, message='None')
2020-08-18T16:21:57+0200 connection to router closed
2020-08-18T16:21:57+0200 Main loop terminated.
python client.py --key .keys/client01-bad.key
2020-08-18T16:21:58+0200 Connecting to ws://localhost:8080/ws: requesting realm=None, authid=None
2020-08-18T16:21:58+0200 initializing component: ComponentConfig(realm=<None>, extra={'channel_binding': None, 'authid': None, 'key': '.keys/client01-bad.key'}, keyring=None, controller=None, shared=None, runner=<autobahn.twisted.wamp.ApplicationRunner object at 0x7f1ce18ff5e0>)
2020-08-18T16:21:58+0200 client public key loaded: fd5bb5a897bf3a7e72d3d07d4f6757af690b0a8b5815f00275101dd8b476b322
2020-08-18T16:21:58+0200 connected to router
2020-08-18T16:21:58+0200 session closed: CloseDetails(reason=<com.example.no_such_user>, message='no principal with matching public key 0xfd5bb5a897bf3a7e72d3d07d4f6757af690b0a8b5815f00275101dd8b476b322')
2020-08-18T16:21:58+0200 connection to router closed
2020-08-18T16:21:58+0200 Main loop terminated.
```
