# MQTT in passthrough mode

In **passthrough mode**, arbitrary MQTT binary payloads are routed "as is" by Crossbar.io without touching or interpretation.

This means, unmodified MQTT clients can connect to Crossbar.io, and events published by these clients are dispatched to both other MQTT subscribers as well as WAMP subscribers.

The MQTT application payload is transmitted without modification passing through the payload as a binary string.

This is using **payload transparency**, a WAMP AP feature implemented by Crossbar.io and AutobahnPython currently.

## When to use

Use **passthrough mode** when you

* can't change the MQTT client code
* want lowest latency
* want lowest load on router

## Payload Codecs

Since the application payload is raw MQTT left untouched by Crossbar.io, WAMP subscribers need to be aware of the binary payload they will receive, and hence will need to have a **payload codec** defined, like in the example:

```python
class MyCodec(object):
    """
    Our codec to encode/decode our custom binary payload. This is needed
    in "payload transparency mode" (a WAMP AP / Crossbar.io feature), so
    the app code is shielded, so you can write your code as usual in Autobahn/WAMP.
    """

    # binary payload format we use in this example:
    # unsigned short + signed int + 8 bytes (all big endian)
    FORMAT = '>Hl8s'

    def encode(self, is_originating, uri, args=None, kwargs=None):
        # Autobahn wants to send custom payload: convert to an instance
        # of EncodedPayload
        payload = struct.pack(self.FORMAT, args[0], args[1], args[2])
        return EncodedPayload(payload, u'mqtt')

    def decode(self, is_originating, uri, encoded_payload):
        # Autobahn has received a custom payload.
        # convert it into a tuple: (uri, args, kwargs)
        return uri, struct.unpack(self.FORMAT, encoded_payload.payload), None

# we need to register our codec!
IPayloadCodec.register(MyCodec)
```

The payload codec then needs to be set on the client session:

```python
class MySession(ApplicationSession):

    def onJoin(self, details):
        self.set_payload_codec(MyCodec())
```

Setting of the payload codec is the only code change required. After that, incoming WAMP events carrying MQTT payloads (via payload transparency mode and `enc_algo="mqtt"`) are automatically and transparently decoded by the configured payload codec, and application code such as event handlers are called as normal, with `args` and `kwargs` already extracted.

Similar, when publishing events from WAMP client app code, the `args` and `kwargs` are encoded automatically and transparently using the configured payload codec, and carried as raw binary MQTT payload (again via payload transparency mode and `enc_algo="mqtt"`) by Crossbar.io and received by unmodified MQTT clients.


## Testing

In a first terminal, start Crossbar.io from this directory:

```console
crossbar start
```

In a second terminal, start a WAMP client that includes a payload codec (`MyCodec`) for the MQTT payload we use in this example:

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

All clients should now seamlessly interoperate, publishing and receiving events in the native MQTT payload format.


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
                "type": "passthrough"
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
