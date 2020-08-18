# WAMP-cryptosign static authentication

*Last tested: 2020/08/18 using Crossbar.io v20.8.2*

-----

WAMP-cryptosign using static configuration example.

In a first terminal, start a [Crossbar.io node](.crossbar/config.json) with a WebSocket transport listening
on port 8080:

```console
make crossbar
```

In a second terminal, start the clients

```console
make clients
```

This will run the following clients in series:

* **Twisted** example: [python client_tx.py](client_tx.py)
* **asyncio** example: [python client_aio.py](client_aio.py)


```console
(cpy382_1) oberstet@intel-nuci7:~/scm/crossbario/crossbar-examples/authentication/cryptosign/static$ make clients
python client_tx.py --realm devices --authid client01@example.com --key .keys/client01.key
2020-08-18T16:09:48+0200 Connecting to ws://localhost:8080/ws: requesting realm=devices, authid=client01@example.com
2020-08-18T16:09:48+0200 initializing component: ComponentConfig(realm=<devices>, extra={'authid': 'client01@example.com', 'key': '.keys/client01.key'}, keyring=None, controller=None, shared=None, runner=<autobahn.twisted.wamp.ApplicationRunner object at 0x7fe7ee63e2e0>)
2020-08-18T16:09:48+0200 client public key loaded: 545efb0a2192db8d43f118e9bf9aee081466e1ef36c708b96ee6f62dddad9122
2020-08-18T16:09:48+0200 connected to router
2020-08-18T16:09:48+0200 authentication challenge received: Challenge(method=cryptosign, extra={'challenge': '6918478679fd1a1be01ee9d3564dd10b85f393fcd56c8b843152621a068b8f5b', 'channel_binding': None})
2020-08-18T16:09:48+0200 session joined:
SessionDetails(realm="devices",
               session=388273487582783,
               authid="client01@example.com",
               authrole="device",
               authmethod="cryptosign",
               authprovider="static",
               authextra={'x_cb_node': 'intel-nuci7-28132', 'x_cb_worker': 'worker001', 'x_cb_peer': 'tcp4:127.0.0.1:38358', 'x_cb_pid': 28142},
               serializer="json.batched",
               transport="websocket",
               resumed=None,
               resumable=None,
               resume_token=None)
2020-08-18T16:09:48+0200 ********************************************************************************
2020-08-18T16:09:48+0200 OK, successfully authenticated with WAMP-cryptosign: realm="devices", authid="client01@example.com", authrole="device"
2020-08-18T16:09:48+0200 ********************************************************************************
2020-08-18T16:09:48+0200 session closed: CloseDetails(reason=<wamp.close.normal>, message='None')
2020-08-18T16:09:48+0200 connection to router closed
2020-08-18T16:09:48+0200 Main loop terminated.
python client_aio.py --realm devices --authid client01@example.com --key .keys/client01.key
Connecting to ws://localhost:8080/ws: requesting realm=devices, authid=client01@example.com
2020-08-18T16:09:49 initializing component: ComponentConfig(realm=<devices>, extra={'authid': 'client01@example.com', 'key': '.keys/client01.key'}, keyring=None, controller=None, shared=None, runner=None)
2020-08-18T16:09:49 client public key loaded: 545efb0a2192db8d43f118e9bf9aee081466e1ef36c708b96ee6f62dddad9122
2020-08-18T16:09:49 connected to router
2020-08-18T16:09:49 authentication challenge received: Challenge(method=cryptosign, extra={'challenge': 'dea3cce01242ce879211814b43c3b1139ccda36df664eb3f20cfc1c41bf5e25c', 'channel_binding': None})
2020-08-18T16:09:49 session joined:
SessionDetails(realm="devices",
               session=4908827272900994,
               authid="client01@example.com",
               authrole="device",
               authmethod="cryptosign",
               authprovider="static",
               authextra={'x_cb_node': 'intel-nuci7-28132', 'x_cb_worker': 'worker001', 'x_cb_peer': 'tcp4:127.0.0.1:38360', 'x_cb_pid': 28142},
               serializer="json.batched",
               transport="websocket",
               resumed=None,
               resumable=None,
               resume_token=None)
2020-08-18T16:09:49 ********************************************************************************
2020-08-18T16:09:49 OK, successfully authenticated with WAMP-cryptosign: realm="devices", authid="client01@example.com", authrole="device"
2020-08-18T16:09:49 ********************************************************************************
2020-08-18T16:09:49 session closed: CloseDetails(reason=<wamp.close.normal>, message='None')
2020-08-18T16:09:49 connection to router closed
python client_tx.py --realm devices --key .keys/client01.key
2020-08-18T16:09:49+0200 Connecting to ws://localhost:8080/ws: requesting realm=devices, authid=None
2020-08-18T16:09:49+0200 initializing component: ComponentConfig(realm=<devices>, extra={'authid': None, 'key': '.keys/client01.key'}, keyring=None, controller=None, shared=None, runner=<autobahn.twisted.wamp.ApplicationRunner object at 0x7fceb9858850>)
2020-08-18T16:09:49+0200 client public key loaded: 545efb0a2192db8d43f118e9bf9aee081466e1ef36c708b96ee6f62dddad9122
2020-08-18T16:09:49+0200 connected to router
2020-08-18T16:09:49+0200 authentication challenge received: Challenge(method=cryptosign, extra={'challenge': '134f9eb1b6626c85a8a340c201afb1b1f06c19b62ed83be8a7990b5dc7c5d4d1', 'channel_binding': None})
2020-08-18T16:09:49+0200 session joined:
SessionDetails(realm="devices",
               session=8260025374496821,
               authid="client01@example.com",
               authrole="device",
               authmethod="cryptosign",
               authprovider="static",
               authextra={'x_cb_node': 'intel-nuci7-28132', 'x_cb_worker': 'worker001', 'x_cb_peer': 'tcp4:127.0.0.1:38362', 'x_cb_pid': 28142},
               serializer="json.batched",
               transport="websocket",
               resumed=None,
               resumable=None,
               resume_token=None)
2020-08-18T16:09:49+0200 ********************************************************************************
2020-08-18T16:09:49+0200 OK, successfully authenticated with WAMP-cryptosign: realm="devices", authid="client01@example.com", authrole="device"
2020-08-18T16:09:49+0200 ********************************************************************************
2020-08-18T16:09:49+0200 session closed: CloseDetails(reason=<wamp.close.normal>, message='None')
2020-08-18T16:09:49+0200 connection to router closed
2020-08-18T16:09:49+0200 Main loop terminated.
python client_aio.py --realm devices --key .keys/client01.key
Connecting to ws://localhost:8080/ws: requesting realm=devices, authid=None
2020-08-18T16:09:49 initializing component: ComponentConfig(realm=<devices>, extra={'authid': None, 'key': '.keys/client01.key'}, keyring=None, controller=None, shared=None, runner=None)
2020-08-18T16:09:49 client public key loaded: 545efb0a2192db8d43f118e9bf9aee081466e1ef36c708b96ee6f62dddad9122
2020-08-18T16:09:49 connected to router
2020-08-18T16:09:49 authentication challenge received: Challenge(method=cryptosign, extra={'challenge': '72a37d186116ad20f50e06d70cd8b309b2f5c33529ddc17e7d663ba790cf8f6a', 'channel_binding': None})
2020-08-18T16:09:49 session joined:
SessionDetails(realm="devices",
               session=2512023573296101,
               authid="client01@example.com",
               authrole="device",
               authmethod="cryptosign",
               authprovider="static",
               authextra={'x_cb_node': 'intel-nuci7-28132', 'x_cb_worker': 'worker001', 'x_cb_peer': 'tcp4:127.0.0.1:38364', 'x_cb_pid': 28142},
               serializer="json.batched",
               transport="websocket",
               resumed=None,
               resumable=None,
               resume_token=None)
2020-08-18T16:09:49 ********************************************************************************
2020-08-18T16:09:49 OK, successfully authenticated with WAMP-cryptosign: realm="devices", authid="client01@example.com", authrole="device"
2020-08-18T16:09:49 ********************************************************************************
2020-08-18T16:09:49 session closed: CloseDetails(reason=<wamp.close.normal>, message='None')
2020-08-18T16:09:49 connection to router closed
(cpy382_1) oberstet@intel-nuci7:~/scm/crossbario/crossbar-examples/authentication/cryptosign/static$
```
