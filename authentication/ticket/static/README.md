# WAMP-Ticket Static Authentication

**WAMP-Ticket static authentication** is a simple cleartext challenge scheme. A client connects to a realm under some `authid` and requests `authmethod = ticket`. Crossbar.io will "challenge" the client, asking for a ticket. The client sends the ticket, and **Crossbar.io will lookup the ticket in the node configuration**.

## How to test

Open a first terminal and start Crossbar.io:

```console
(python279_1)oberstet@thinkpad-t430s:~/scm/crossbario/crossbarexamples/authentication/ticket/static$ crossbar start
...
2015-12-29T12:42:42+0100 [Router       4343] Backend session joined: SessionDetails(realm = realm1, session = 479412185559674, authid = None, authrole = backend, authmethod = None)
...
```

Above runs a router together with a [backend](backend.py) component. As can be seen from the log above, the backend component has joined `realm1` under effective `authrole = backend`.

Open a second terminal and start [client](client.py):

```console
(python279_1)oberstet@thinkpad-t430s:~/scm/crossbario/crossbarexamples/authentication/ticket/static$ python client.py
2015-12-29T12:44:48+0100 Client session connected. Starting WAMP-Ticket authentication on realm 'realm1' as principal 'joe' ..
2015-12-29T12:44:48+0100 WAMP-Ticket challenge received: Challenge(method = ticket, extra = {})
2015-12-29T12:44:48+0100 Client session joined: SessionDetails(realm = realm1, session = 7957364806440431, authid = joe, authrole = frontend, authmethod = ticket)
...
```

As the log shows, the client was authenticating using `authmethod = ticket` as `authid = joe` and joined the realm under role `authrole = frontend`.

Open [http://localhost:8080](http://localhost:8080) in your browser, and check the JavaScript console output:

```console
Ok, AutobahnJS loaded 0.9.9
onchallenge ticket Object {}
connected session with ID 7678305144433231
authenticated using method 'ticket' and provider 'static'
authenticated with authid 'joe' and authrole 'frontend'
...
```

Again, the log reveals that the client was authenticated using `authmethod = ticket`, `authid = joe` and `authrole = frontend`.


## How it works

Static WAMP-Ticket is activated in Crossbar.io by configuring a respective `auth` attribute on the transport:

```json
"auth": {
    "ticket": {
        "type": "static",
        "principals": {
            "joe": {
                "ticket": "secret!!!",
                "role": "frontend"
            }
        }
    }
}
```

With `type = static`, a `principals` element is required: a dictionary mapping `authid` to a dictionary with two elements: `ticket`, the secret being shared, and `role`, the `authrole` that will be assigned in case of successful authentication.

The `authrole` the client is assigned determines the permissions the client has. E.g. consider this part of the [node configuration](.crossbar/config.json):

```json
"realms": [
   {
      "name": "realm1",
      "roles": [
         {
            "name": "backend",
            "permissions": [
            ...
            ]
         },
         {
            "name": "frontend",
            "permissions": [
            ...
            ]
         }
      ]
   }
]
```

There are two roles configured: `frontend` and `backend`. The AutobahnJS based Web "UI" [index.html](web/index.html), as well as the AutobahnPython based [client](client.py) both connect under role `frontend`, while the AutobahnPython based [backend](backend.py) connect under role `backend`.

### Authentication Errors

When the `authid` the client announces isn't known, you get

```console
(python279_1)oberstet@thinkpad-t430s:~/scm/crossbario/crossbarexamples/authentication/ticket/static$ python client.py
2015-12-29T13:14:42+0100 Client session connected. Starting WAMP-Ticket authentication on realm 'realm1' as principal 'client1' ..
2015-12-29T13:14:42+0100 Client session left: CloseDetails(reason = wamp.error.not_authorized, message = 'no principal with authid 'client1' in principal database'')
2015-12-29T13:14:42+0100 Client session disconnected.
2015-12-29T13:14:42+0100 Main loop terminated.
```

When the `authid` is known, but the ticket the client presented is invalid, you get

```console
(python279_1)oberstet@thinkpad-t430s:~/scm/crossbario/crossbarexamples/authentication/ticket/static$ python client.py
2015-12-29T13:16:24+0100 Client session connected. Starting WAMP-Ticket authentication on realm 'realm1' as principal 'client1' ..
2015-12-29T13:16:24+0100 WAMP-Ticket challenge received: Challenge(method = ticket, extra = {})
2015-12-29T13:16:24+0100 Client session left: CloseDetails(reason = wamp.error.not_authorized, message = 'WAMP-Ticket ticket is invalid'')
2015-12-29T13:16:24+0100 Client session disconnected.
2015-12-29T13:16:24+0100 Main loop terminated.
```

### Using environment variables

The `ticket` field contains sensitive information, and you might want to prefer holding that value in an environment variable. This is possible by defining a principal like this:

```json
"client2": {
   "ticket": "${MYTICKET}",
   "role": "frontend"
}
```

A client with a value for `ticket` that matches the pattern `${..}` will be interpreted as an environment variable, and Crossbar.io tries to set the configuration item from this environment variable.

To this this variant with the example here, start Crossbar.io in a first terminal:

```console
MYTICKET=geheim crossbar start
```

You will see a log line

```console
2015-12-29T14:50:41+0100 [Controller   5765] Configuration 'auth.ticket.principals["client2"].ticket' set from environment variable $MYTICKET
```

that indicates an configuration item was indeed set from an environment variable. If the environment variable is missing, you get

```console
2015-12-29T14:50:14+0100 [Controller   5754] Environment variable $MYTICKET not set - needed in configuration 'auth.ticket.principals["client2"].ticket'
```

Now start the client in a second terminal:

```console
MYTICKET=geheim python client.py client2
```

You should see the client successfully authenticate:

```console
(python279_1)oberstet@thinkpad-t430s:~/scm/crossbario/crossbarexamples/authentication/ticket/static$ MYTICKET=geheim python client.py client2
Principal 'client2' using ticket 'geheim'
(<type 'unicode'>, <type 'unicode'>)
2015-12-29T14:52:26+0100 Client session connected. Starting WAMP-Ticket authentication on realm 'realm1' as principal 'client2' ..
2015-12-29T14:52:26+0100 WAMP-Ticket challenge received: Challenge(method = ticket, extra = {})
2015-12-29T14:52:26+0100 Client session joined: SessionDetails(realm = realm1, session = 1274456341345787, authid = client2, authrole = frontend, authmethod = ticket)
...
```
