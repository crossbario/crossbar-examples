# Using MQTT with Crossbar.io

## Introduction

Crossbar.io is a multi-protocol router with support for MQTT Version 3.1.1.

You can use Crossbar.io both as a standalone MQTT broker, and to integrate MQTT clients with a WAMP based system.

The latter is possible as Crossbar.io includes a MQTT bridge that allows WAMP and MQTT publishers and subscribers talk to each other transparently.

This opens up whole new possibilities, eg immediately integrate MQTT client devices into a larger WAMP based application, add native remote procedure call functionality to an MQTT based system or gradually migrating an existing MQTT system towards WAMP.


## Payload Mapping

MQTT is completely agnostic to application payload. Application payload in MQTT is a (single) binary string.

In WAMP, application payload is carried in structured form (args, kwargs), and auxiliary information for the interaction (call, invocation, publish, event) is exposed as well to enable rich, standard and custom semantics.

So there is an impedance mismatch, and part of what is required is a mapping or transformation between application payloads.

In general, application payload between MQTT and WAMP can be transformed in three layers:

* within the WAMP client library or WAMP app code ("passthrough mode")
* within the MQTT client library or MQTT app code ("native mode")
* within the router ("dynamic mode")

Crossbar.io supports all three modes, and the modes are configurable in an URI tree to operate new code along legacy code which enables a gradual migration path for app code.

In **[passthrough mode](passthrough)**, MQTT payloads are transmitted in *payload transparency mode* on the wire, which means, Crossbar.io will not touch the (arbitrary binary) MQTT payload at all.

In **[native mode](native)**, MQTT payloads are converted between WAMP structured application payload and MQTT binary payload using a statically configured serializer such as JSON, CBOR, MessagePack or UBJSON.

In **[dynamic mode](dynamic)**, MQTT payloads are converted between arbitrary binary and WAMP structured application payload by calling into a user provided *payload transformer function*, which can be implemented in any WAMP supported language.


## Requirements

The examples make use of the MQTT bridge now included with Crossbar.io 17.4.1 and later.

For testing, we use the following two MQTT clients:

* [Paho Python](https://eclipse.org/paho/clients/python/)
* [MQTT.js](https://github.com/mqttjs/MQTT.js)

To install Paho Python, create a fresh virtualenv and do:

```console
pip install paho-mqtt
```

The NodeJS dependencies for the JavaScript based examples need to be installed by doing:

    npm install


## Testing

There are 3 Crossbar.io test node configurations

* [passthrough](passthrough)
* [native](native)
* [dynamic](dynamic)

and 8 example clients:

* [mqtt-client.js](mqtt-client.js)
* [mqtt-client.py](mqtt-client.py)
* [mqtt-client-wamp.js](mqtt-client-wamp.js)
* [mqtt-client-wamp.py](mqtt-client-wamp.py)
* [wamp-client.js](wamp-client.js)
* [wamp-client.py](wamp-client.py)
* [wamp-client-mqtt.js](wamp-client-mqtt.js)
* [wamp-client-mqtt.py](wamp-client-mqtt.py)

These can be run in the following combinations:

### Testing passthrough mode

In a first terminal, run Crossbar.io from the [passthrough](passthrough) directory.

In further terminals, run any of the following example clients

* [mqtt-client.js](mqtt-client.js)
* [mqtt-client.py](mqtt-client.py)
* [wamp-client-mqtt.js](wamp-client-mqtt.js)
* [wamp-client-mqtt.py](wamp-client-mqtt.py)

In passthrough mode, Crossbar.io is completely unaware of the MQTT payload it transfers, and the MQTT clients are left unchanged completely, but the WAMP clients need to have codecs set for the incoming native MQTT payload to get parsed.


### Testing native mode

In a first terminal, run Crossbar.io from the [native](native) directory.

In further terminals, run any of the following example clients

* [mqtt-client-wamp.js](mqtt-client-wamp.js)
* [mqtt-client-wamp.py](mqtt-client-wamp.py)
* [wamp-client.py](wamp-client.py)
* [wamp-client.js](wamp-client.js)

In native mode, Crossbar.io will parse the binary MQTT application payload according to the configured serializer, and expect a dict with `args` and `kwargs`, and possibly options.


### Testing dynamic mode

In a first terminal, run Crossbar.io from the [dynamic](dynamic) directory.

In further terminals, run any of the following example clients

* [mqtt-client.js](mqtt-client.js)
* [mqtt-client.py](mqtt-client.py)
* [wamp-client.js](wamp-client.js)
* [wamp-client.py](wamp-client.py)

In dynamic mode, both unmodified MQTT and unmodified WAMP clients talk with each other. This is possible as Crossbar.io calls into a custom payload codec provided as two user WAMP procedures.
