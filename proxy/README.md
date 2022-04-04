# Proxy Workers

## Introduction

It is now possible to use "proxy" workers to terminate incoming client
connections. This can be used to offload some pressure from
router-workers or to do protocol translation (e.g. from json etc
serializers to more efficient CBOR or msgpack serializers on the
backend).

## High Level Explanation

Proxy workers can also directly serve "web" type requests that
otherwise would push load onto a "normal" WebSocket router-worker.

To configure a proxy worker, include a stanza like::

            "type": "proxy",
            "backends": [
              ...
            ],
            "transports": [
              ...
            ]
        },

A proxy worker can include "web", "archive", "nodeinfo" etc stanzans
in the "transport" section -- anything a router worker has. It must
have at least one "backend" configured -- this is where it will direct
incoming "websocket" connections. You can include any number of proxy
workers.

You may include a "realm" key in a backend; if it is included, only
incoming connections to that realm will be directed to the configured
backend. If you include no "realm" key, it is the "default" backend
and all connections will be directed there (unless another matching
backend is found via realm).

This means: you can have a single backend per realm on an efficient
local transport with an efficient serializer, while fronting "real"
client requests with multiple proxy workers. These can server web /
archive / nodeinfo requests directly and will de-serialize incoming
messages and possibly re-serialize them differently for the backend.

A single worker must serve a single realm, so this allows a certain
amount of scaling (each proxy worker will be its own process, so can
take advantage of a separate CPU core, if available).

## The Full Example

In the full example configuration available here, there are two proxy
workers which also serve an Autobahn archive, some normal Web content
and listen on WebSocket connections for clients. There is a single
backend for realm `realm1` which listens on two different (local)
Unix-domain sockets: one at `router.sock` (via RawSocket) and one at
`routerws.sock` (via WebSocket). This would likely be just a single
rawsocket in a more "production" configuration; the two exist for
demonstration purposes.

To run the example, start at least three shells:

 - in one, run "crossbar start" in this directory
 - in a second, run "python client-publish.py"
 - in a third, run "python client-listen.py"

You may run more instances of the listen or publish scripts if you
wish. Try shutting down various parts and starting them again.

### Web Resources

The example node configuration will start proxy workers, not only listening for incoming
WebSocket connections (and proxying those to backend router workers), but _also_ serves
various other web services:

1. [http://localhost:8443](http://localhost:8443): **path "/", type "static"** - static web files
1. [http://localhost:8443/info](http://localhost:8443/info): **path "info", type "info"** - node info page
1. [http://localhost:8443/ws](http://localhost:8443/ws): **path "ws", type "websocket-proxy"** - websocket endpoint (of listening proxy)
1. [http://localhost:8443/autobahn/autobahn/autobahn.js](http://localhost:8443/autobahn/autobahn/autobahn.js): **path "autobahn", type "archive"** - ZIP archive resource
1. [http://localhost:8443/autobahn/autobahn-xbr/autobahn-xbr.js](http://127.0.0.1:8443/autobahn/autobahn-xbr/autobahn-xbr.js): **path "autobahn", type "archive"** - ZIP archive resource (same archive file, but different contained file referenced)

## Testing

### Router

```
(cpy39_1) (base) oberstet@intel-nuci7:~/scm/crossbario/crossbar-examples/proxy$ make run_config5
crossbar start --config=config5.json

2022-04-04T18:28:45+0200 [Controller  37690] Stale Crossbar.io PID file (pointing to non-existing process with PID 37389) /home/oberstet/scm/crossbario/crossbar-examples/proxy/.crossbar/node.pid removed
2022-04-04T18:28:45+0200 [Controller  37690]
2022-04-04T18:28:45+0200 [Controller  37690]     :::::::::::::::::
2022-04-04T18:28:45+0200 [Controller  37690]           :::::          _____                 __              _
2022-04-04T18:28:45+0200 [Controller  37690]     :::::   :   :::::   / ___/______  ___ ___ / /  ___ _____  (_)__
2022-04-04T18:28:45+0200 [Controller  37690]     :::::::   :::::::  / /__/ __/ _ \(_-<(_-</ _ \/ _ `/ __/ / / _ \
2022-04-04T18:28:45+0200 [Controller  37690]     :::::   :   :::::  \___/_/  \___/___/___/_.__/\_,_/_/ (_)_/\___/
2022-04-04T18:28:45+0200 [Controller  37690]           :::::
2022-04-04T18:28:45+0200 [Controller  37690]     :::::::::::::::::   Crossbar.io v22.4.1.dev1 [19000101-0000000]
2022-04-04T18:28:45+0200 [Controller  37690]
2022-04-04T18:28:45+0200 [Controller  37690]     Copyright (c) 2013-2022 Crossbar.io Technologies GmbH. Licensed under EUPLv1.2.
2022-04-04T18:28:45+0200 [Controller  37690]
2022-04-04T18:28:45+0200 [Controller  37690] Booting standalone node .. <crossbar.node.main._run_command_start>
2022-04-04T18:28:45+0200 [Controller  37690] Node configuration loaded [config_source=localfile, config_path=/home/oberstet/scm/crossbario/crossbar-examples/proxy/.crossbar/config5.json]
2022-04-04T18:28:45+0200 [Controller  37690] Node key files exist and are valid. Node public key is 0xee07d793bc3031374e4419c46b6a2e7656b54e290dce7bd22f6c32a5141999f5
2022-04-04T18:28:45+0200 [Controller  37690] Node key loaded from /home/oberstet/scm/crossbario/crossbar-examples/proxy/.crossbar/key.priv
2022-04-04T18:28:45+0200 [Controller  37690] Entering event reactor ...
2022-04-04T18:28:45+0200 [Controller  37690] Starting node .. [<crossbar.node.node.Node.start>]
2022-04-04T18:28:45+0200 [Controller  37690] Node ID intel-nuci7-37690 set from hostname/pid
2022-04-04T18:28:45+0200 [Controller  37690] RouterFactory.start_realm: router created for realm "crossbar"
...
2022-04-04T18:28:50+0200 [Controller  37690] Ok, local node configuration ran successfully.
2022-04-04T18:28:50+0200 [Controller  37690] <crossbar.node.node.Node.boot>::NODE_BOOT_COMPLETE
2022-04-04T18:28:51+0200 [Proxy       37727] <crossbar.worker.proxy.ProxyFrontendSession.onOpen> Proxy frontend session connected from peer tcp4:127.0.0.1:49816
2022-04-04T18:28:51+0200 [Proxy       37727] <crossbar.worker.proxy.ProxyFrontendSession._process_Hello> processed authmethod "ticket" using <class 'crossbar.router.auth.ticket.PendingAuthTicket'>: Challenge(method=ticket, extra={})
2022-04-04T18:28:51+0200 [Proxy       37727] <crossbar.worker.proxy.ProxyFrontendSession._accept> Frontend session accepted (Accept(realm=<realm1>, authid=<user1>, authrole=<user>, authmethod=ticket, authprovider=static, authextra={})) - opening proxy backend session ...
2022-04-04T18:28:52+0200 [Proxy       37727] <crossbar.worker.proxy.ProxyController.map_backend>: ok, proxy backend connection opened mapping frontend session to realm "realm1", authrole "user"
2022-04-04T18:28:52+0200 [Proxy       37727] <crossbar.worker.proxy.ProxyFrontendSession._accept.<locals>._backend_connected> Proxy backend session authenticating using authmethods=['anonymous-proxy']
2022-04-04T18:28:52+0200 [Router      37699] Router attached new session to realm "realm1" (session=3747191555396008, authid="user1", authrole="user", authmethod="anonymous-proxy", authprovider="static") <crossbar.router.router.Router.attach>
2022-04-04T18:28:52+0200 [Proxy       37727] <crossbar.worker.proxy.ProxyFrontendSession._accept.<locals>._backend_connected.<locals>._on_backend_joined> Ok, proxy backend session 3747191555396008 joined!
2022-04-04T18:29:13+0200 [Proxy       37718] <crossbar.worker.proxy.ProxyFrontendSession.onOpen> Proxy frontend session connected from peer tcp4:127.0.0.1:49818
2022-04-04T18:29:13+0200 [Proxy       37718] <crossbar.worker.proxy.ProxyFrontendSession._process_Hello> processed authmethod "ticket" using <class 'crossbar.router.auth.ticket.PendingAuthTicket'>: Challenge(method=ticket, extra={})
2022-04-04T18:29:13+0200 [Proxy       37718] <crossbar.worker.proxy.ProxyFrontendSession._accept> Frontend session accepted (Accept(realm=<realm1>, authid=<user2>, authrole=<user>, authmethod=ticket, authprovider=static, authextra={})) - opening proxy backend session ...
2022-04-04T18:29:13+0200 [Proxy       37718] <crossbar.worker.proxy.ProxyController.map_backend>: ok, proxy backend connection opened mapping frontend session to realm "realm1", authrole "user"
2022-04-04T18:29:13+0200 [Proxy       37718] <crossbar.worker.proxy.ProxyFrontendSession._accept.<locals>._backend_connected> Proxy backend session authenticating using authmethods=['anonymous-proxy']
2022-04-04T18:29:13+0200 [Router      37699] Router attached new session to realm "realm1" (session=381140739751398, authid="user2", authrole="user", authmethod="anonymous-proxy", authprovider="static") <crossbar.router.router.Router.attach>
2022-04-04T18:29:13+0200 [Proxy       37718] <crossbar.worker.proxy.ProxyFrontendSession._accept.<locals>._backend_connected.<locals>._on_backend_joined> Ok, proxy backend session 381140739751398 joined!
2022-04-04T18:31:45+0200 [Container   37708] add2() called with 1 and 2
2022-04-04T18:32:03+0200 [Container   37708] add2() called with 1 and 2
2022-04-04T18:32:32+0200 [Container   37708] add2() called with 1 and 2
2022-04-04T18:32:40+0200 [Container   37708] add2() called with 1 and 2
2022-04-04T18:32:58+0200 [Container   37708] add2() called with 23 and 666
2022-04-04T18:35:10+0200 [Proxy       37727] <crossbar.worker.proxy.ProxyFrontendSession.onClose>(wasClean=False)
2022-04-04T18:35:10+0200 [Router      37699] Router detached session from realm "realm1" (session=3747191555396008, detached_session_ids=1, authid="user1", authrole="user", authmethod="anonymous-proxy", authprovider="static") <crossbar.router.router.Router.detach>
...
```

### WAMP

Publisher:

```
(cpy39_1) (base) oberstet@intel-nuci7:~/scm/crossbario/crossbar-examples/proxy$ make run_publish_ws_cbor
python client-publish.py websocket-cbor
2022-04-04T18:29:13+0200 joined:
2022-04-04T18:29:13+0200 SessionDetails(realm="realm1",
2022-04-04T18:29:13+0200                session=381140739751398,
2022-04-04T18:29:13+0200                authid="user2",
2022-04-04T18:29:13+0200                authrole="user",
2022-04-04T18:29:13+0200                authmethod="ticket",
2022-04-04T18:29:13+0200                authprovider="static",
2022-04-04T18:29:13+0200                authextra={'x_cb_node': 'intel-nuci7-37690', 'x_cb_worker': 'worker001', 'x_cb_peer': 'unix', 'x_cb_pid': 37699, 'x_cb_proxy_node': 'intel-nuci7-37690', 'x_cb_proxy_worker': 'worker003', 'x_cb_proxy_peer': 'tcp4:127.0.0.1:49818', 'x_cb_proxy_pid': 37718},
2022-04-04T18:29:13+0200                serializer="cbor",
2022-04-04T18:29:13+0200                transport="websocket",
2022-04-04T18:29:13+0200                resumed=None,
2022-04-04T18:29:13+0200                resumable=None,
2022-04-04T18:29:13+0200                resume_token=None)
2022-04-04T18:29:13+0200 pid 37791 publish 0 to 'demo.foo'
2022-04-04T18:29:14+0200 pid 37791 publish 1 to 'demo.foo'
2022-04-04T18:29:15+0200 pid 37791 publish 2 to 'demo.foo'
2022-04-04T18:29:16+0200 pid 37791 publish 3 to 'demo.foo'
2022-04-04T18:29:17+0200 pid 37791 publish 4 to 'demo.foo'
...
```

Subscriber:

```
(cpy39_1) (base) oberstet@intel-nuci7:~/scm/crossbario/crossbar-examples/proxy$ make run_subscribe_ws_cbor
python client-subscribe.py websocket-cbor
2022-04-04T18:28:52+0200 joined:
2022-04-04T18:28:52+0200 SessionDetails(realm="realm1",
2022-04-04T18:28:52+0200                session=3747191555396008,
2022-04-04T18:28:52+0200                authid="user1",
2022-04-04T18:28:52+0200                authrole="user",
2022-04-04T18:28:52+0200                authmethod="ticket",
2022-04-04T18:28:52+0200                authprovider="static",
2022-04-04T18:28:52+0200                authextra={'x_cb_node': 'intel-nuci7-37690', 'x_cb_worker': 'worker001', 'x_cb_peer': 'unix', 'x_cb_pid': 37699, 'x_cb_proxy_node': 'intel-nuci7-37690', 'x_cb_proxy_worker': 'worker004', 'x_cb_proxy_peer': 'tcp4:127.0.0.1:49816', 'x_cb_proxy_pid': 37727},
2022-04-04T18:28:52+0200                serializer="cbor",
2022-04-04T18:28:52+0200                transport="websocket",
2022-04-04T18:28:52+0200                resumed=None,
2022-04-04T18:28:52+0200                resumable=None,
2022-04-04T18:28:52+0200                resume_token=None)
2022-04-04T18:28:52+0200 subscribed
2022-04-04T18:28:52+0200 .
2022-04-04T18:29:13+0200 demo.foo: (37791, 0) {'foo': '0x049afc5411486d570f0a', 'baz': b'\x04\x9a\xfcT\x11HmW\x0f\n'}
2022-04-04T18:29:14+0200 .
2022-04-04T18:29:14+0200 demo.foo: (37791, 1) {'foo': '0x9824b5c7ccabcf2681e8', 'baz': b'\x98$\xb5\xc7\xcc\xab\xcf&\x81\xe8'}
2022-04-04T18:29:15+0200 .
2022-04-04T18:29:15+0200 demo.foo: (37791, 2) {'foo': '0xae66837a14ea26c392c2', 'baz': b'\xaef\x83z\x14\xea&\xc3\x92\xc2'}
2022-04-04T18:29:16+0200 .
2022-04-04T18:29:16+0200 demo.foo: (37791, 3) {'foo': '0xd6019fcdd69a8b431567', 'baz': b'\xd6\x01\x9f\xcd\xd6\x9a\x8bC\x15g'}
2022-04-04T18:29:17+0200 .
2022-04-04T18:29:17+0200 demo.foo: (37791, 4) {'foo': '0x3471967bacf45964faf4', 'baz': b'4q\x96{\xac\xf4Yd\xfa\xf4'}
2022-04-04T18:29:18+0200 .
2022-04-04T18:29:18+0200 demo.foo: (37791, 5) {'foo': '0x28c720af47adac1cb050', 'baz': b'(\xc7 \xafG\xad\xac\x1c\xb0P'}
2022-04-04T18:29:19+0200 .
2022-04-04T18:29:19+0200 demo.foo: (37791, 6) {'foo': '0x9f56c1cbaec763abc253', 'baz': b'\x9fV\xc1\xcb\xae\xc7c\xab\xc2S'}
2022-04-04T18:29:20+0200 .
2022-04-04T18:29:20+0200 demo.foo: (37791, 7) {'foo': '0x064b3a5736660d2a15f8', 'baz': b'\x06K:W6f\r*\x15\xf8'}
...
```

### ReST Bridge

```
(cpy39_1) (base) oberstet@intel-nuci7:~/scm/crossbario/crossbar-examples/proxy$ make run_test_restbridge_call
curl -H "Content-Type: application/json" \
	-d '{"procedure": "com.example.add2", "args": [23, 666]}' \
	http://localhost:8443/call
{"args":[689]}
```

