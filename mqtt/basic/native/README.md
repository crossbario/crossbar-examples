# MQTT in native mode

In **native mode**, MQTT binary payloads are expected to contain a serialized WAMP aware payload, and this is parsed by Crossbar.io according to the configured serialized, such a CBOR or MessagePack, ..

This means, WAMP aware MQTT clients can connect to Crossbar.io, and events published by these clients are dispatched to both other WAMP aware MQTT subscribers as well as native WAMP subscribers.

The WAMP aware MQTT client can use many of WAMPs advanced features, such us subscriber black-/whitelisting.

## When to use

Use **native mode** when you

* want advanced WAMP features also for MQTT clients
* can change the MQTT client code
* can't change the WAMP client code

## WAMP Payloads

WAMP-aware MQTT clients will publish events with a application payload consisting of a dictionary serialized using a agreed serializer such as CBOR.

The dictionary can contain attributes

```json
{
    "args": [],
    "kwargs": {},
    "exclude": null,
    "exclude_authid": null,
    "exclude_authrole": null,
    "eligible": null,
    "eligible_authid": null,
    "eligible_authrole'": null
}
```

## Testing

In a first terminal, start Crossbar.io from this directory:

```console
crossbar start
```

In a second terminal, start a WAMP aware MQTT client:

```console
python mqtt-client-wamp.py
node mqtt-client-wamp.js
```

Then start a native, unmodified WAMP client

```console
python wamp-client.py
node wamp-client.js
```

All clients should now seamlessly interoperate, publishing and receiving events in the native WAMP payload format.


## Configuration

Here is an example that configured **native mode** on a MQTT transport for all mapped URI having the empty string as prefix, which means all URIs:

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
                "type": "native",
                "serializer": "cbor"
            }
        }
    }
}
```

You can configure different modes on different URI prefixes by adding more entries to the `payload_mapping` attribute. Hence, the keys of the `payload_mapping` dict are interpreted as WAMP URI prefixes, and the matching will alway be on the longest matching prefix over the configured keys.

**IMPORTANT: When no matching payload mapping could be found for the URI of an event to be transferred, the event is discarded. This applies to any event directions, including MQTT-to-MQTT traffic.**

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
                    "type": "native",
                    "serializer": "cbor"
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
