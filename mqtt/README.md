# Using MQTT with Crossbar.io

Crossbar.io is a multi-protocol router with support for MQTT Version 3.1.1. You can use Crossbar.io both as a standalone MQTT broker, and to integrate MQTT clients with a WAMP based system.

In **[passthrough mode](passthrough)**, MQTT payloads are transmitted in *payload transparency mode* on the wire, which means, Crossbar.io will not touch the (arbitrary binary) MQTT payload at all.

In **[dynamic mode](dynamic)**, MQTT payloads are converted between arbitrary binary and WAMP structured application payload by calling into a user provided *payload transformer function*, which can be implemented in any WAMP supported language.

In **[static mode](static)**, MQTT payloads are converted between WAMP structured application payload and MQTT binary payload using a statically configured serializer such as JSON, CBOR, MessagePack or UBJSON.


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
