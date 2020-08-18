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
