# Configuring serializers in Crossbar.io

Crossbar.io has support for these WAMP serializers:

* JSON
* MessagePack
* UBJSON
* CBOR

By default, Crossbar.io will speak all serializers installed. But it's also possible to restrict the set of spoken serializers, which this example does.

Consider this part of the node configuration in [./crossbar/config.json](./crossbar/config.json):

```json
"ws": {
    "type": "websocket",
    "serializers": ["ubjson"]
}
```

This will disable all serializers but UBJSON.

To test, start Crossbar.io in a first terminal (from this directory):

```console
crossbar start
```

Then, in a second terminal, start a test client connecting to Crossbar.io:

```console
(cpy351_1) oberstet@corei7ub1310:~/scm/crossbario/crossbarexamples/serializers$ python client.py
2016-04-21T19:50:47+0200 ClientSession joined: SessionDetails(realm=<realm1>, session=8315432505316575, authid=<9H5A-K99W-F54K-6FRU-A7SC-EGTE>, authrole=<anonymous>, authmethod=anonymous, authprovider=static, authextra=None)
2016-04-21T19:50:47+0200

*** Transport is using 'ubjson.batched' serializer ***

2016-04-21T19:50:47+0200 ClientSession left: CloseDetails(reason=<wamp.close.normal>, message='None')
2016-04-21T19:50:47+0200 ClientSession disconnected
2016-04-21T19:50:47+0200 Main loop terminated.
```

You can also start Crossbar.io with loglevel "trace":

```console
crossbar start --loglevel=trace
```

This will dump an insane amount of messages, but you'll see:

```
HTTP/1.1 101 Switching Protocols
Server: Crossbar/0.13.2
X-Powered-By: AutobahnPython/0.13.1
Upgrade: WebSocket
Connection: Upgrade
Sec-WebSocket-Protocol: wamp.2.ubjson.batched
Sec-WebSocket-Accept: m3vvAYqSx9sxQyjf1EV+7q53r5o=
```

This is part of the WebSocket opening handshake - the WebSocket server (Crossbar.io) accepting the client with `Sec-WebSocket-Protocol: wamp.2.ubjson.batched`, which hints at the serializer used for WAMP.
