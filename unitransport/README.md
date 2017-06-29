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
    "type": "universal",
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

This example is using Docker for quick startup.

To start Crossbar.io, open a shell and change to the [crossbar](crossbar) directory. Then type:

```console
make test
```

To start a first microservice written in Python using AutobahnPython, open another shell and change to the [service-py](service-py) directory. Then type:

```console
make test
```

To start a second microservice written in C++ using AutobahnC++, open another shell and change to the [service-cpp](service-cpp) directory. Then type:

```console
make test
```

To start a third microservice written in JavaScript using AutobahnJS, open another shell and change to the [service-js](service-js) directory. Then type:

```console
make test
```
