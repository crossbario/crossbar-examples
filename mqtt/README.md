# Using MQTT with Crossbar.io

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

### Testing native mode

In a first terminal, run Crossbar.io from the [native](native) directory.

In further terminals, run any of the following example clients

* [mqtt-client-wamp.js](mqtt-client-wamp.js)
* [mqtt-client-wamp.py](mqtt-client-wamp.py)
* [wamp-client.py](wamp-client.py)
* [wamp-client.js](wamp-client.js)

### Testing dynamic mode

In a first terminal, run Crossbar.io from the [dynamic](dynamic) directory.

In further terminals, run any of the following example clients

* [mqtt-client.js](mqtt-client.js)
* [mqtt-client.py](mqtt-client.py)
* [wamp-client.js](wamp-client.js)
* [wamp-client.py](wamp-client.py)


### Appendix

MQTT is completely agnostic to application payload. Application payload in MQTT is a (single) binary string.

In WAMP, application payload is carried in structured form (args, kwargs), and auxiliary information for the interaction (call, invocation, publish, event) is exposed as well to enable rich, standard and custom semantics.

So there is an impedance mismatch, and part of what is required is a mapping or transformation between application payloads.

In general, application payload between MQTT and WAMP can be transformed in three layers:

* within the WAMP client library or WAMP app code
* within the MQTT client library or MQTT app code
* within the router

Crossbar.io supports all three modes, and the modes are configurable in an URI tree to operate new code along legacy code which enables a gradual migration path for app code.

## Introduction

Crossbar.io is a multi-protocol router with support for MQTT Version 3.1.1. You can use Crossbar.io both as a standalone MQTT broker, and to integrate MQTT clients with a WAMP based system in different modes:

* payload transparency (enc_algo `"passthrough"`)
* payload mapping (enc_algo `"native"`)
* payload transformer (enc_algo `"dynamic"`)

In **[passthrough mode](passthrough)**, MQTT payloads are transmitted in *payload transparency mode* on the wire, which means, Crossbar.io will not touch the (arbitrary binary) MQTT payload at all.

In **[dynamic mode](dynamic)**, MQTT payloads are converted between arbitrary binary and WAMP structured application payload by calling into a user provided *payload transformer function*, which can be implemented in any WAMP supported language.

In **[native mode](native)**, MQTT payloads are converted between WAMP structured application payload and MQTT binary payload using a statically configured serializer such as JSON, CBOR, MessagePack or UBJSON.

```json
{
    "transports": [
        {
            "type": "mqtt",
            "endpoint": {
                "type": "tcp",
                "port": 1883
            },
            "options": {
                "realm": "realm1",
                "role": "anonymous",
                "payload": {
                    "": {
                        "type": "passthrough"
                    },
                    "test/": {
                        "type": "dynamic",
                        "encoder": "com.example.mqtt.encode",
                        "decoder": "com.example.mqtt.decode"
                    },
                    "api/test": {
                        "type": "native",
                        "serializer": "cbor"
                    }
                }
            }
        }
    ]
}
```

```json
{
    "transports": [
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
                    "payload": {
                        "": {
                            "type": "passthrough"
                        },
                        "test/": {
                            "type": "dynamic",
                            "encoder": "com.example.mqtt.encode",
                            "decoder": "com.example.mqtt.decode"
                        },
                        "api/test": {
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
    ]
}
```

## Testing

For testing, we use the following two MQTT clients from the [Eclipse Paho project](https://eclipse.org/paho/):

* [Paho Python](https://eclipse.org/paho/clients/python/)
* [Paho C](https://eclipse.org/paho/clients/c/)
* [MQTT.js](https://github.com/mqttjs/MQTT.js)

To install Paho Python, create a fresh virtualenv and do:

```console
pip install paho-mqtt
```

To build and install Paho C, do:

```console
cd /tmp
git clone https://github.com/eclipse/paho.mqtt.c.git
cd org.eclipse.paho.mqtt.c
make
sudo make install
```

> This will install shared libraries into `/usr/local/lib` and headers into `/usr/local/include`



# MQTT Bridge

Crossbar.io includes a MQTT bridge that not only makes it a full scale, great MQTT broker on its own, but also allows WAMP and MQTT publishers and subscribers talk to each other transparently.

This opens up whole new possibilities, eg immediately integrate MQTT client devices into a larger WAMP based application or system

## Demo

The demo make use of the MQTT bridge now included with Crossbar.io 17.2.1 and later.

You need to install `paho-mqtt` to run the MQTT client which you can
do via pip:

   pip install paho-mqtt

Then, with the Crossbar.io router running from [examples/router](https://github.com/crossbario/autobahn-python/tree/master/examples/router) dir you
can start up either the WAMP or MQTT client first (ideally in
different shells):

   python wamp-client.py
   python mqtt-client.py

They both subscribe to `mqtt.test_topic` and then publish some data to
that same topic (so try starting them in different orders etc).

## Configuration

To configure MQTT in Crossbar.io, add a MQTT transport item to a router worker like here:


```
"transports": [
    {
        "type": "mqtt",
        "endpoint": {
            "type": "tcp",
            "port": 1883
        },
        "options": {
            "realm": "crossbardemo",
            "role": "anonymous"
        }
    }
]
```

Besides the listening endpoint configuration, you can configure the mapping to a WAMP realm.


# note that unlike Autobahn and Crossbar, this MQTT client is threaded
# / synchronous
# http://www.steves-internet-guide.com/loop-python-mqtt-client/
# http://www.steves-internet-guide.com/subscribing-topics-mqtt-client/
# http://www.steves-internet-guide.com/publishing-messages-mqtt-client/
# http://www.steves-internet-guide.com/mqtt/
# http://www.steves-internet-guide.com/into-mqtt-python-client/

