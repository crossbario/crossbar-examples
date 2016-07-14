# Universal Transport

This example demonstrates the new **universal transport** in Crossbar.io.

The universal transport allows to service multiple protocols on one listening endpoint, such as the default TLS listening port:

* WAMP-over-RawSocket
* WAMP-over-WebSocket
* Web Resources

All of above can be combined with different endpoints for

* TCP
* TLS
* Unix domain socket

and with different serializers (with support for heterogenous clients)

* CBOR
* MessagePack
* UBJSON
* JSON

## Configuration

The new transport is configured like in this snippet from this example configuration:

```json
{
    "type": "unisocket",
    "endpoint": {
        "type": "tcp",
        "port": 8080
    },
    "rawsocket": {
    },
    "websocket": {
        "/ws": {
            "type": "websocket"
        }
    },
    "web": {
        "paths": {
            "/": {
                "type": "static",
                "directory": ".."
            }
        }
    }
}
```

## How to run

We are working on a Docker setup.
