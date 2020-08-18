# WAMP-CRA with function-based authentication

*Last tested: 2020/08/18 using Crossbar.io v20.8.2*

-----

WAMP-CRA with function-based authentication, using a custom authenticator.

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

The client will be run twice, once using a valid key, and once using an invalid secret:

```console
(cpy382_1) oberstet@intel-nuci7:~/scm/crossbario/crossbar-examples/authentication/wampcra/function$ make clients
MYSECRET="secret123" python client.py client1
User 'client1' using secret 'secret123'
2020-08-18T22:47:36+0200 Client session connected. Starting WAMP-CRA authentication on realm 'realm1' as user 'client1' ..
2020-08-18T22:47:37+0200 WAMP-CRA challenge received: Challenge(method=wampcra, extra={'challenge': '{"authid": "client1", "authrole": "frontend", "authmethod": "wampcra", "authprovider": "function", "session": 5140915082691617, "nonce": "4YoonXhegaqWtY4JLJrEzvgiVCtWsnaDPgDCxzsbkFOcWJi3z/nRMyhKOj/vas0R", "timestamp": "2020-08-18T20:47:37.395Z"}'})
2020-08-18T22:47:37+0200 Client session joined:
2020-08-18T22:47:37+0200 SessionDetails(realm="realm1",
2020-08-18T22:47:37+0200                session=5140915082691617,
2020-08-18T22:47:37+0200                authid="client1",
2020-08-18T22:47:37+0200                authrole="frontend",
2020-08-18T22:47:37+0200                authmethod="wampcra",
2020-08-18T22:47:37+0200                authprovider="function",
2020-08-18T22:47:37+0200                authextra={'x_cb_node': 'intel-nuci7-11256', 'x_cb_worker': 'worker001', 'x_cb_peer': 'tcp4:127.0.0.1:41602', 'x_cb_pid': 11268},
2020-08-18T22:47:37+0200                serializer="cbor.batched",
2020-08-18T22:47:37+0200                transport="websocket",
2020-08-18T22:47:37+0200                resumed=None,
2020-08-18T22:47:37+0200                resumable=None,
2020-08-18T22:47:37+0200                resume_token=None)
2020-08-18T22:47:37+0200 call result: 5
2020-08-18T22:47:37+0200 registration failed - this is expected: ApplicationError(error=<wamp.error.not_authorized>, args=['session (session_id=5140915082691617, authid="client1", authrole="frontend") is not authorized to register procedure "com.example.mul2" on realm "realm1"'], kwargs={}, enc_algo=None, callee=None, callee_authid=None, callee_authrole=None, forward_for=None)
2020-08-18T22:47:37+0200 ok, event published to topic com.example.topic1
2020-08-18T22:47:37+0200 ok, event published to topic com.foobar.topic1
2020-08-18T22:47:37+0200 publication to topic com.example.topic2 failed - this is expected: ApplicationError(error=<wamp.error.not_authorized>, args=["session not authorized to publish to topic 'com.example.topic2'"], kwargs={}, enc_algo=None, callee=None, callee_authid=None, callee_authrole=None, forward_for=None)
2020-08-18T22:47:37+0200 publication to topic com.foobar.topic2 failed - this is expected: ApplicationError(error=<wamp.error.not_authorized>, args=["session not authorized to publish to topic 'com.foobar.topic2'"], kwargs={}, enc_algo=None, callee=None, callee_authid=None, callee_authrole=None, forward_for=None)
2020-08-18T22:47:37+0200 Client session left: CloseDetails(reason=<wamp.close.normal>, message='None')
2020-08-18T22:47:37+0200 Client session disconnected.
2020-08-18T22:47:37+0200 Main loop terminated.
MYSECRET="wrongpassword" python client.py client1
User 'client1' using secret 'wrongpassword'
2020-08-18T22:47:37+0200 Client session connected. Starting WAMP-CRA authentication on realm 'realm1' as user 'client1' ..
2020-08-18T22:47:37+0200 WAMP-CRA challenge received: Challenge(method=wampcra, extra={'challenge': '{"authid": "client1", "authrole": "frontend", "authmethod": "wampcra", "authprovider": "function", "session": 5172291906109194, "nonce": "Fk74AGfl8r0nTm2sxaFZc+1N24UyvwbjdCzIfTrtj9ZMi5CKZ2s1xe2w543gcsIh", "timestamp": "2020-08-18T20:47:37.869Z"}'})
2020-08-18T22:47:37+0200 Client session left: CloseDetails(reason=<wamp.error.not_authorized>, message='WAMP-CRA signature is invalid')
2020-08-18T22:47:37+0200 Client session disconnected.
2020-08-18T22:47:37+0200 Main loop terminated.
(cpy382_1) oberstet@intel-nuci7:~/scm/crossbario/crossbar-examples/authentication/wampcra/function$
```
