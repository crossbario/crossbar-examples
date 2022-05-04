# WAMP-CRA Static Authentication

*Last tested: 2020/08/18 using Crossbar.io v20.8.2*

-----

Demonstrates WAMP-CRA with static credentials from node configuration file:

* [Python client](client.py)
* [JS client](web/index.html)


```console
(cpy382_1) oberstet@intel-nuci7:~/scm/crossbario/crossbar-examples/authentication/wampcra/static$ make clients
MYSECRET="secret123" python client.py client1
2020-08-18T21:34:18+0200 Client session connected. Starting WAMP-CRA authentication on realm 'realm1' as user 'client1' ..
2020-08-18T21:34:18+0200 WAMP-CRA challenge received: Challenge(method=wampcra, extra={'challenge': '{"authid": "client1", "authrole": "frontend", "authmethod": "wampcra", "authprovider": "static", "session": 2167280380730926, "nonce": "f9EimNk1VCsKrH+3iHo+ImfCdJIbuxFOpZJTkLVkpAEXRtxYmMXcqV8iti1UEVUB", "timestamp": "2020-08-18T19:34:18.625Z"}'})
2020-08-18T21:34:18+0200 Client session joined:
2020-08-18T21:34:18+0200 SessionDetails(realm="realm1",
2020-08-18T21:34:18+0200                session=2167280380730926,
2020-08-18T21:34:18+0200                authid="client1",
2020-08-18T21:34:18+0200                authrole="frontend",
2020-08-18T21:34:18+0200                authmethod="wampcra",
2020-08-18T21:34:18+0200                authprovider="static",
2020-08-18T21:34:18+0200                authextra={'x_cb_node': 'intel-nuci7-6879', 'x_cb_worker': 'worker001', 'x_cb_peer': 'tcp4:127.0.0.1:40708', 'x_cb_pid': 6889},
2020-08-18T21:34:18+0200                serializer="cbor.batched",
2020-08-18T21:34:18+0200                transport="websocket",
2020-08-18T21:34:18+0200                resumed=None,
2020-08-18T21:34:18+0200                resumable=None,
2020-08-18T21:34:18+0200                resume_token=None)
2020-08-18T21:34:18+0200 call result: 5
2020-08-18T21:34:18+0200 registration failed - this is expected: ApplicationError(error=<wamp.error.not_authorized>, args=['session (session_id=2167280380730926, authid="client1", authrole="frontend") is not authorized to register procedure "com.example.mul2" on realm "realm1"'], kwargs={}, enc_algo=None, callee=None, callee_authid=None, callee_authrole=None, forward_for=None)
2020-08-18T21:34:18+0200 ok, event published to topic com.example.topic1
2020-08-18T21:34:18+0200 ok, event published to topic com.foobar.topic1
2020-08-18T21:34:18+0200 publication to topic com.example.topic2 failed - this is expected: ApplicationError(error=<wamp.error.not_authorized>, args=["session not authorized to publish to topic 'com.example.topic2'"], kwargs={}, enc_algo=None, callee=None, callee_authid=None, callee_authrole=None, forward_for=None)
2020-08-18T21:34:18+0200 publication to topic com.foobar.topic2 failed - this is expected: ApplicationError(error=<wamp.error.not_authorized>, args=["session not authorized to publish to topic 'com.foobar.topic2'"], kwargs={}, enc_algo=None, callee=None, callee_authid=None, callee_authrole=None, forward_for=None)
2020-08-18T21:34:18+0200 Client session left: CloseDetails(reason=<wamp.close.normal>, message='None')
2020-08-18T21:34:18+0200 Client session disconnected.
2020-08-18T21:34:18+0200 Main loop terminated.
MYSECRET="wrongpassword" python client.py client1
2020-08-18T21:34:19+0200 Client session connected. Starting WAMP-CRA authentication on realm 'realm1' as user 'client1' ..
2020-08-18T21:34:19+0200 WAMP-CRA challenge received: Challenge(method=wampcra, extra={'challenge': '{"authid": "client1", "authrole": "frontend", "authmethod": "wampcra", "authprovider": "static", "session": 5031675066974572, "nonce": "5Ix7W2ejbdGXutc1xbV1reLLkK7LMf7JlL9AzOiC6x5Qcz06WggM8tK3i8bXVJyB", "timestamp": "2020-08-18T19:34:19.103Z"}'})
2020-08-18T21:34:19+0200 Client session left: CloseDetails(reason=<wamp.error.not_authorized>, message='WAMP-CRA signature is invalid')
2020-08-18T21:34:19+0200 Client session disconnected.
2020-08-18T21:34:19+0200 Main loop terminated.
(cpy382_1) oberstet@intel-nuci7:~/scm/crossbario/crossbar-examples/authentication/wampcra/static$
```

## Meta API

```
2022-05-04T00:29:21+0200 [Proxy      104034] <autobahn.twisted.websocket.WebSocketAdapterProtocol.connectionMade> connection established for peer="tcp4:127.0.0.1:45674"
2022-05-04T00:29:21+0200 [Proxy      104034] <crossbar.router.protocol.WampWebSocketServerProtocol.onConnect>: no tracking/authentication cookie cbtid found in HTTP request headers!
2022-05-04T00:29:21+0200 [Proxy      104034] <crossbar.router.protocol.WampWebSocketServerProtocol.onConnect>: setting new cookie cbtid=g2G9WNnUSfPdIgDkLiNtgDqO;max-age=604800
2022-05-04T00:29:21+0200 [Proxy      104034] <crossbar.router.protocol.WampWebSocketServerProtocol.onConnect> cookie-based authentication enabled, but cookie is not authenticated yet
2022-05-04T00:29:21+0200 [Proxy      104034] <crossbar.worker.proxy.ProxyFrontendSession.onOpen> proxy frontend session connected from peer tcp4:127.0.0.1:45674
2022-05-04T00:29:21+0200 [Proxy      104034] <crossbar.worker.proxy.ProxyFrontendSession.frontend_accepted> proxy frontend session accepted (Accept(realm=<realm1>, authid=<client1>, authrole=<frontend>, authmethod=wampcra, authprovider=static, authextra=None))
2022-05-04T00:29:21+0200 [Proxy      104034] <crossbar.worker.proxy.make_backend_connection> proxy connecting to backend with backend_config=
{'transport': {'endpoint': {'path': 'crossbar.sock', 'type': 'unix'},
               'serializer': 'cbor',
               'type': 'rawsocket',
               'url': 'ws://localhost'}}
2022-05-04T00:29:21+0200 [Proxy      104034] <crossbar.worker.proxy.ProxyFrontendSession.frontend_accepted.<locals>.backend_connected> proxy backend session authenticating with authmethods=['anonymous-proxy'], pubkey=c71289fe71920793da6c95086cc71dafd96aeaa171831154f5a5301a6fc20387: proxy_authid="client1", proxy_authrole="frontend", proxy_realm="realm1"
2022-05-04T00:29:21+0200 [Router     104013] <crossbar.router.router.Router.attach> new session attached for realm="realm1", session=6287901217990880, authid="client1", authrole="frontend", authmethod="anonymous-proxy", authprovider="static", authextra=
{'transport': {'channel_framing': 'websocket',
               'channel_id': {},
               'channel_serializer': None,
               'channel_type': 'tcp',
               'http_cbtid': 'g2G9WNnUSfPdIgDkLiNtgDqO',
               'http_headers_received': {'cache-control': 'no-cache',
                                         'connection': 'Upgrade',
                                         'host': 'localhost:8080',
                                         'pragma': 'no-cache',
                                         'sec-websocket-extensions': 'permessage-deflate; '
                                                                     'client_no_context_takeover; '
                                                                     'client_max_window_bits',
                                         'sec-websocket-key': 'WSNfuVrqbukehRyNsQghVA==',
                                         'sec-websocket-protocol': 'wamp.2.json',
                                         'sec-websocket-version': '13',
                                         'upgrade': 'WebSocket',
                                         'user-agent': 'AutobahnPython/22.4.1'},
               'http_headers_sent': {'Set-Cookie': 'cbtid=g2G9WNnUSfPdIgDkLiNtgDqO;max-age=604800'},
               'is_secure': False,
               'is_server': True,
               'own': None,
               'own_fd': -1,
               'own_pid': 104034,
               'own_tid': 104034,
               'peer': 'tcp4:127.0.0.1:45674',
               'peer_cert': None,
               'websocket_extensions_in_use': [{'client_max_window_bits': 13,
                                                'client_no_context_takeover': False,
                                                'extension': 'permessage-deflate',
                                                'is_server': True,
                                                'mem_level': 5,
                                                'server_max_window_bits': 13,
                                                'server_no_context_takeover': False}],
               'websocket_protocol': 'wamp.2.json'},
 'x_cb_node': 'intel-nuci7-104003',
 'x_cb_peer': 'unix',
 'x_cb_pid': 104013,
 'x_cb_worker': 'test_router1'}
2022-05-04T00:29:21+0200 [Proxy      104034] <crossbar.worker.proxy.ProxyBackendSession.onJoin> proxy backend session joined (authmethod=anonymous-proxy, authprovider=static): realm="realm1", authid="client1", authrole="frontend"
2022-05-04T00:29:21+0200 [Container  104045] <monitor.MyMonitor.onJoin.<locals>.on_session_join>: new session joined, session_info=
{'authextra': {'transport': {'channel_framing': 'websocket',
                             'channel_id': {},
                             'channel_serializer': None,
                             'channel_type': 'tcp',
                             'http_cbtid': 'g2G9WNnUSfPdIgDkLiNtgDqO',
                             'http_headers_received': {'cache-control': 'no-cache',
                                                       'connection': 'Upgrade',
                                                       'host': 'localhost:8080',
                                                       'pragma': 'no-cache',
                                                       'sec-websocket-extensions': 'permessage-deflate; '
                                                                                   'client_no_context_takeover; '
                                                                                   'client_max_window_bits',
                                                       'sec-websocket-key': 'WSNfuVrqbukehRyNsQghVA==',
                                                       'sec-websocket-protocol': 'wamp.2.json',
                                                       'sec-websocket-version': '13',
                                                       'upgrade': 'WebSocket',
                                                       'user-agent': 'AutobahnPython/22.4.1'},
                             'http_headers_sent': {'Set-Cookie': 'cbtid=g2G9WNnUSfPdIgDkLiNtgDqO;max-age=604800'},
                             'is_secure': False,
                             'is_server': True,
                             'own': None,
                             'own_fd': -1,
                             'own_pid': 104034,
                             'own_tid': 104034,
                             'peer': 'tcp4:127.0.0.1:45674',
                             'peer_cert': None,
                             'websocket_extensions_in_use': [{'client_max_window_bits': 13,
                                                              'client_no_context_takeover': False,
                                                              'extension': 'permessage-deflate',
                                                              'is_server': True,
                                                              'mem_level': 5,
                                                              'server_max_window_bits': 13,
                                                              'server_no_context_takeover': False}],
                             'websocket_protocol': 'wamp.2.json'},
               'x_cb_node': 'intel-nuci7-104003',
               'x_cb_peer': 'unix',
               'x_cb_pid': 104013,
               'x_cb_worker': 'test_router1'},
 'authid': 'client1',
 'authmethod': 'anonymous-proxy',
 'authprovider': 'static',
 'authrole': 'frontend',
 'realm': 'realm1',
 'resumable': False,
 'resume_token': None,
 'resumed': False,
 'serializer': None,
 'session': 6287901217990880,
 'transport': {'channel_framing': 'rawsocket',
               'channel_id': {},
               'channel_serializer': 'cbor',
               'channel_type': 'tcp',
               'http_cbtid': None,
               'http_headers_received': None,
               'http_headers_sent': None,
               'is_secure': False,
               'is_server': None,
               'own': None,
               'own_fd': -1,
               'own_pid': 104013,
               'own_tid': 104013,
               'peer': 'unix',
               'peer_cert': None,
               'websocket_extensions_in_use': None,
               'websocket_protocol': 'wamp.2.cbor'}}
2022-05-04T00:29:21+0200 [Router     104013] <crossbar.router.service.RouterServiceAgent.session_get> session 6287901217990880 in active memory
2022-05-04T00:29:21+0200 [Container  104045] <monitor.MyMonitor.onJoin.<locals>.on_session_join>: ok, event data identical to getter API!
2022-05-04T00:29:22+0200 [Router     104013] add2() called with 2 and 3
2022-05-04T00:29:22+0200 [Router     104013] event received on com.foobar.topic2: hello
2022-05-04T00:29:22+0200 [Router     104013] event received on com.foobar.topic2: hello
2022-05-04T00:29:22+0200 [Router     104013] Router detached session from realm "realm1" (session=6287901217990880, detached_session_ids=1, authid="client1", authrole="frontend", authmethod="anonymous-proxy", authprovider="static") <crossbar.router.router.Router.detach>
2022-05-04T00:29:22+0200 [Proxy      104034] <crossbar.worker.proxy.ProxyFrontendSession.onClose> proxy frontend session closed (wasClean=True)
2022-05-04T00:29:22+0200 [Proxy      104034] <autobahn.twisted.websocket.WebSocketAdapterProtocol.connectionLost> connection lost for peer="tcp4:127.0.0.1:45674", closed cleanly
2022-05-04T00:29:22+0200 [Container  104045] <monitor.MyMonitor.onJoin.<locals>.on_session_leave>: existing session left, session_id=6287901217990880
2022-05-04T00:29:22+0200 [Proxy      104034] <crossbar.worker.proxy.ProxyBackendSession.onClose> proxy backend session closed (wasClean=True)
2022-05-04T00:29:22+0200 [Router     104013] <crossbar.router.service.RouterServiceAgent.session_get> session 6287901217990880 loaded from database
2022-05-04T00:29:22+0200 [Container  104045] <monitor.MyMonitor.onJoin.<locals>.on_session_leave> session data retrieved for closed session:
{'authextra': {'transport': {'channel_framing': 'websocket',
                             'channel_id': {},
                             'channel_serializer': None,
                             'channel_type': 'tcp',
                             'http_cbtid': 'g2G9WNnUSfPdIgDkLiNtgDqO',
                             'http_headers_received': {'cache-control': 'no-cache',
                                                       'connection': 'Upgrade',
                                                       'host': 'localhost:8080',
                                                       'pragma': 'no-cache',
                                                       'sec-websocket-extensions': 'permessage-deflate; '
                                                                                   'client_no_context_takeover; '
                                                                                   'client_max_window_bits',
                                                       'sec-websocket-key': 'WSNfuVrqbukehRyNsQghVA==',
                                                       'sec-websocket-protocol': 'wamp.2.json',
                                                       'sec-websocket-version': '13',
                                                       'upgrade': 'WebSocket',
                                                       'user-agent': 'AutobahnPython/22.4.1'},
                             'http_headers_sent': {'Set-Cookie': 'cbtid=g2G9WNnUSfPdIgDkLiNtgDqO;max-age=604800'},
                             'is_secure': False,
                             'is_server': True,
                             'own': None,
                             'own_fd': -1,
                             'own_pid': 104034,
                             'own_tid': 104034,
                             'peer': 'tcp4:127.0.0.1:45674',
                             'peer_cert': None,
                             'websocket_extensions_in_use': [{'client_max_window_bits': 13,
                                                              'client_no_context_takeover': False,
                                                              'extension': 'permessage-deflate',
                                                              'is_server': True,
                                                              'mem_level': 5,
                                                              'server_max_window_bits': 13,
                                                              'server_no_context_takeover': False}],
                             'websocket_protocol': 'wamp.2.json'},
               'x_cb_node': 'intel-nuci7-104003',
               'x_cb_peer': 'unix',
               'x_cb_pid': 104013,
               'x_cb_worker': 'test_router1'},
 'authid': 'client1',
 'authmethod': 'anonymous-proxy',
 'authprovider': 'static',
 'authrole': 'frontend',
 'realm': 'realm1',
 'resumable': False,
 'resume_token': None,
 'resumed': False,
 'serializer': None,
 'session': 6287901217990880,
 'transport': {'channel_framing': 'rawsocket',
               'channel_id': {},
               'channel_serializer': 'cbor',
               'channel_type': 'tcp',
               'http_cbtid': None,
               'http_headers_received': None,
               'http_headers_sent': None,
               'is_secure': False,
               'is_server': None,
               'own': None,
               'own_fd': -1,
               'own_pid': 104013,
               'own_tid': 104013,
               'peer': 'unix',
               'peer_cert': None,
               'websocket_extensions_in_use': None,
               'websocket_protocol': 'wamp.2.cbor'}}
2022-05-04T00:29:22+0200 [Container  104045] <monitor.MyMonitor.onJoin.<locals>.on_session_leave> ok, event data identical to getter API
```
