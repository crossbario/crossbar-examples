# Proxy Workers

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
rawsocket in a moer "production" configuration; the two exist for
demonstration purposes.

The `client.py` will start a client pointing at the proxy workers, yet
ultimately contact the backend and publish some messages. You could
start multiple `client.py` instances.
