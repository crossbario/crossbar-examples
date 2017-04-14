# MQTT in passthrough mode

In **passthrough mode**, arbitrary MQTT binary payloads are routed "as is" by Crossbar.io without touching or interpretation.

This means, unmodified MQTT clients can connect to Crossbar.io, and events published by these clients are dispatched to both other MQTT subscribers as well as WAMP subscribers.

The MQTT application payload is transmitted without modification passing through the payload as a binary string.

This is using a WAMP AP feature: **payload transparency**.

WAMP subscribers need to be aware of the binary payload they will receive, and hence will need to have a **payload codec** set on the client session.

## Testing

In a first terminal, start Crossbar.io from this directory:

```console
crossbar start
```

In a second termina, start a WAMP client that includes a payload codec (`MyCodec`) for the MQTT payload we use in this example:

```console
python wamp-client-mqtt.py
```

Then start a native, unmodified MQTT client in Python

```console
python mqtt-client.py
```

or JavaScript under NodeJS

```console
node mqtt-client.js
```

## Configuration

Here is an example that configured **passthrough mode** on a MQTT transport for all mapped URI having the empty string as prefix, which means all URIs:

```json
{
    "type": "mqtt",
        "endpoint": {
        "type": "tcp",
        "port": 1883
    },
    "options": {
        "realm": "realm1",
        "role": "anonymous",
        "payload_mapping": {
            "": {
                "match": "prefix",
                "type": "passthrough"
            }
        }
    }
}
```

You can configured different modes on different URI patterns by adding more entries to the `payload_mapping` attribute.

Similar to configuring payload modes for standalone MQTT transport, the same `options` dictionary attribute can be used with MQTT factories on **universal transports**:

```json
{
    "type": "universal",
    "endpoint": {
        "type": "tcp",
        "port": 8080
    },
    "mqtt": {
        "options": {
            "realm": "realm1",
            "role": "anonymous",
            "payload_mapping": {
                "": {
                    "match": "prefix",
                    "type": "passthrough"
                }
            }
        }
    },
    "rawsocket": {
        "serializers": [
            "cbor", "msgpack", "ubjson", "json"
        ]
    },
    "websocket": {
        "ws": {
            "type": "websocket",
            "serializers": [
                "cbor", "msgpack", "ubjson", "json"
            ]
        }
    },
    "web": {
        "paths": {
            "/": {
                "type": "static",
                "directory": "..",
                "options": {
                    "enable_directory_listing": true
                }
            }
        }
    }
}
```
