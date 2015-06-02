# Publishing Events

## Basic Usage

This example demonstrates how to publish real-time notifications to Web clients via [WAMP/WebSocket](http://wamp.ws/) using the HTTP bridge built into [Crossbar.io](https://github.com/crossbario/crossbar).

The [test.py](test.py) script creates a new Crossbar.io pusher client

```python
client = crossbarconnect.Client("http://127.0.0.1:8080/push")
```

and uses this to submit events to be distributed by Crossbar.io to WAMP clients in real-time:

```python
client.push("com.myapp.topic1", "Hello, world!")
```

Under the hood, `crossbarconnect.Client.push` will prepare and issue a plain old HTTP/POST request to the Crossbar.io HTTP bridge.
