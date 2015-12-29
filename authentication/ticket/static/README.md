# WAMP-Ticket Static Authentication

There are two roles configured: `frontend` and `backend`. The AutobahnJS based Web "UI", as well as the AutobahnPython based [client](client.py) both connect under role `frontend`, while the AutobahnPython based [backend](backend.py) connect under role `backend`.

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
