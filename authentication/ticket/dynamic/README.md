# WAMP-Ticket Dynamic Authentication

**WAMP-Ticket dynamic** authentication is a simple cleartext challenge scheme. A client connects to a realm under some `authid` and requests `authmethod = ticket`. Crossbar.io will "challenge" the client, asking for a ticket. The client sends the ticket, and **Crossbar.io will in turn call a user implemented WAMP procedure for the actual verification of the ticket**.

## How to test

Open a first terminal and start Crossbar.io:

```console
(python279_1)oberstet@thinkpad-t430s:~/scm/crossbario/crossbarexamples/authentication/ticket/dynamic$ crossbar start
...
2015-12-29T15:34:02+0100 [Router       6367] WAMP-Ticket dynamic authenticator registered!
...
2015-12-29T15:34:02+0100 [Router       6367] Backend session joined: SessionDetails(realm = realm1, session = 5634489438796591, authid = None, authrole = backend, authmethod = None)
...
```

Above runs a router together with an [authenticator](authenticator.py) and a [backend](backend.py) component. As can be seen from the log above, the dynamic authenticator was registered, and the backend component has joined `realm1` under effective `authrole = backend`.

Open a second terminal and start [client](client.py):

```console
(python279_1)oberstet@thinkpad-t430s:~/scm/crossbario/crossbarexamples/authentication/ticket/dynamic$ python client.py
Principal 'client1' using ticket '123sekret'
2015-12-29T15:36:50+0100 Client session connected. Starting WAMP-Ticket authentication on realm 'realm1' as principal 'client1' ..
2015-12-29T15:36:50+0100 WAMP-Ticket challenge received: Challenge(method = ticket, extra = {})
2015-12-29T15:36:50+0100 Client session joined: SessionDetails(realm = realm1, session = 8960834490945301, authid = client1, authrole = frontend, authmethod = ticket)
...
```

As the log shows, the client was authenticating using `authmethod = ticket` as `authid = client1` and joined the realm under role `authrole = frontend`.
