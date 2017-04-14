# MQTT in dynamic mode

In **dynamic mode**, arbitrary MQTT binary payloads are received by Crossbar.io, transformed by a user codec procedure pair, and further routed as regular WAMP traffic by Crossbar.io.

This means, unmodified MQTT clients can connect to Crossbar.io, and events published by these clients are dispatched to both other unmodified MQTT subscribers as well as unmodified WAMP subscribers - each in their native format!

The MQTT application payload is transformed by user code that is called by Crossbar.io to convert the native MQTT application payload to and from WAMP. Crossbar.io will cache a converted payload within the message.

When the payload codec procedures registered and configured for MQTT co-reside within the routing core, and hence are written in Python/Twisted (the same as Crossbar.io), then the overhead and added latency of the router side, and cached payload conversion is very low.

## When to use

Use **dynamic mode** when you

* can't change the MQTT client code
* can't change the WAMP client code
* want low latency (under restrictions)

## Payload Codecs

Since the application payload received from MQTT clients is raw MQTT, and unmodified WAMP subscribers are unaware of the binary payload they would receive, the MQTT payload needs to be converted back and forth to WAMP application payloads at the router side.

And since Crossbar.io has no idea of the application specific binary MQTT payload, in **dynamic mode** Crossbar.io is configured to call user provided procedures:

* encoder
* decoder

to convert the payload formats. Crossbar.io will call into these user provided procedures only once per message and will cache the result inside the message object for further use. Further, when the payload codec procedures are registered from a component that co-resides and runs embedded with the router worker, then the call overhead is diminishing as well.

Here is an example of a user codec:

```python
class MyCodec(ApplicationSession):

    @inlineCallbacks
    def onJoin(self, details):

        def decode(mapped_topic, topic, payload):
            pid, seq, ran = struct.unpack(FORMAT, payload)
            options = {
                'args': [pid, seq, ran]
            }
            self.log.info('decode {mapped_topic}: {from_mqtt} -> {to_wamp}', mapped_topic=mapped_topic, from_mqtt=payload, to_wamp=options)
            return options

        def encode(mapped_topic, topic, args, kwargs):
            pid, seq, ran = args
            payload = struct.pack(FORMAT, pid, seq, ran)
            self.log.info('encode {mapped_topic}: {from_wamp} -> {to_mqtt}', mapped_topic=mapped_topic, from_wamp={u'args': args}, to_mqtt=payload)
            return payload

        prefix = u'com.example.mqtt'

        yield self.register(decode, u'{}.decode'.format(prefix))
        yield self.register(encode, u'{}.encode'.format(prefix))

        self.log.info("MyCodec ready!")
```

This payload codec then needs to be run, and the encoder and decoder procedures it registers when run need to be configured as payload codec procedures in the MQTT transport configuration:

```json
"mqtt": {
    "options": {
        "realm": "realm1",
        "role": "anonymous",
        "payload_mapping": {
            "": {
                "type": "dynamic",
                "realm": "codec",
                "encoder": "com.example.mqtt.encode",
                "decoder": "com.example.mqtt.decode"
            }
        }
    }
}
```

When Crossbar.io receives a MQTT payload, it will call into the user decoder to let it be decoded into WAMP `args` and `kwargs`, and possibly other `options`.

When Crossbar.io wants to send a MQTT payload, it will call into the user encoder to let it encode the WAMP `args`, `kwargs` and possibly other `options` into a MQTT binary `payload`.


## Testing

In a first terminal, start Crossbar.io from this directory:

```console
crossbar start
```

In a second terminal, start any of the native MQTT or WAMP clients:

```console
python wamp-client.py
python mqtt-client.py
node wamp-client.js
node mqtt-client.js
```

All clients should now seamlessly interoperate, publishing and receiving events in the native MQTT payload format or native WAMP payload format respectively.


## Configuration

Here is an example that configured **dynamic mode** on a MQTT transport for all mapped URI having the empty string as prefix, which means all URIs:

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
                "type": "dynamic",
                "realm": "codec",
                "encoder": "com.example.mqtt.encode",
                "decoder": "com.example.mqtt.decode"
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
                    "type": "dynamic",
                    "realm": "codec",
                    "encoder": "com.example.mqtt.encode",
                    "decoder": "com.example.mqtt.decode"
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
