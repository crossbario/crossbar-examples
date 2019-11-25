# Session Statistics Example

Crossbar.io is able to automatically track WAMP session traffic, eg the number ot (rated) WAMP messages
sent or rceived. Please see [here](https://crossbar.io/docs/Session-Statistics/).

To run this demo, start the Crossbar.io node:

```console
make crossbar
```

This will start a router worker, as well as a container worker hosting our statistics monitoring backend.

The, in a second terminal, start the test client - which will produce WAMP traffic which is printed by the monitor;

```console
make test
```

Files:

* [.crossbar/config.json](.crossbar/config.json): node configuration with statistics tracking enabled on realm `realm1`
* [monitor.py](monitor.py): monitoring client that subscribes to `wamp.session.*` meta events, including traffic statistics
* [client.py](client.py): application example client used to generate traffic that is tracked by the session statistics feature in Crossbar.io
