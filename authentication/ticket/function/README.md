# WAMP-ticket with dynamic authentication

*Last tested: 2020/08/18 using Crossbar.io v20.8.2*

-----

WAMP-ticket with dynamic authentication, using a custom authenticator.

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
(cpy382_1) oberstet@intel-nuci7:~/scm/crossbario/crossbar-examples/authentication/ticket/function$ make clients
MYTICKET="secret123" python client.py client1
Principal 'client1' using ticket 'secret123'
2020-08-18T21:07:49+0200 Client session connected. Starting WAMP-Ticket authentication on realm 'realm1' as principal 'client1' ..
2020-08-18T21:07:49+0200 WAMP-Ticket challenge received: Challenge(method=ticket, extra={})
2020-08-18T21:07:49+0200 Client session joined:
2020-08-18T21:07:49+0200 SessionDetails(realm="realm1",
2020-08-18T21:07:49+0200                session=1624768318416923,
2020-08-18T21:07:49+0200                authid="client1",
2020-08-18T21:07:49+0200                authrole="frontend",
2020-08-18T21:07:49+0200                authmethod="ticket",
2020-08-18T21:07:49+0200                authprovider="function",
2020-08-18T21:07:49+0200                authextra={'x_cb_node': 'intel-nuci7-5703', 'x_cb_worker': 'worker001', 'x_cb_peer': 'tcp4:127.0.0.1:40392', 'x_cb_pid': 5714},
2020-08-18T21:07:49+0200                serializer="json.batched",
2020-08-18T21:07:49+0200                transport="websocket",
2020-08-18T21:07:49+0200                resumed=None,
2020-08-18T21:07:49+0200                resumable=None,
2020-08-18T21:07:49+0200                resume_token=None)
2020-08-18T21:07:49+0200 call result: 5
2020-08-18T21:07:49+0200 registration failed (this is expected!) ApplicationError(error=<wamp.error.not_authorized>, args=['session (session_id=1624768318416923, authid="client1", authrole="frontend") is not authorized to register procedure "com.example.mul2" on realm "realm1"'], kwargs={}, enc_algo=None, callee=None, callee_authid=None, callee_authrole=None, forward_for=None)
2020-08-18T21:07:49+0200 ok, event published to topic com.example.topic1
2020-08-18T21:07:49+0200 ok, event published to topic com.foobar.topic1
2020-08-18T21:07:49+0200 publication to topic com.example.topic2 failed (this is expected!) ApplicationError(error=<wamp.error.not_authorized>, args=["session not authorized to publish to topic 'com.example.topic2'"], kwargs={}, enc_algo=None, callee=None, callee_authid=None, callee_authrole=None, forward_for=None)
2020-08-18T21:07:49+0200 publication to topic com.foobar.topic2 failed (this is expected!) ApplicationError(error=<wamp.error.not_authorized>, args=["session not authorized to publish to topic 'com.foobar.topic2'"], kwargs={}, enc_algo=None, callee=None, callee_authid=None, callee_authrole=None, forward_for=None)
2020-08-18T21:07:49+0200 Client session left: CloseDetails(reason=<wamp.close.normal>, message='None')
2020-08-18T21:07:49+0200 Client session disconnected.
2020-08-18T21:07:49+0200 Main loop terminated.
MYTICKET="wrongpassword" python client.py client1
Principal 'client1' using ticket 'wrongpassword'
2020-08-18T21:07:49+0200 Client session connected. Starting WAMP-Ticket authentication on realm 'realm1' as principal 'client1' ..
2020-08-18T21:07:49+0200 WAMP-Ticket challenge received: Challenge(method=ticket, extra={})
2020-08-18T21:07:49+0200 Client session left: CloseDetails(reason=<com.example.invalid_ticket>, message='could not authenticate session - invalid ticket 'wrongpassword' for principal client1')
2020-08-18T21:07:49+0200 Client session disconnected.
2020-08-18T21:07:49+0200 Main loop terminated.
(cpy382_1) oberstet@intel-nuci7:~/scm/crossbario/crossbar-examples/authentication/ticket/function$
```
