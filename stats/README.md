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

Here is example output

```console
2019-11-25T15:38:28+0100 [Router      15259] Router.attach(session=3463278813717336)
2019-11-25T15:38:28+0100 [Router      15259] Router.attach(session=3463278813717336): attached session 3463278813717336 to router realm "realm1"
2019-11-25T15:38:28+0100 [Router      15259] WAMP session statistics ENABLED (rated_message_size=256, trigger_after_rated_messages=10, trigger_after_duration=0, trigger_on_join=True, trigger_on_leave=True)
2019-11-25T15:38:28+0100 [Container   15270] >>>>>> MONITOR : session joined
{'authextra': {'x_cb_node_id': None,
               'x_cb_peer': 'tcp4:127.0.0.1:21310',
               'x_cb_pid': 15259},
 'authid': 'MTHR-ANE9-CFAR-6U4C-SV3M-X5AL',
 'authmethod': 'anonymous',
 'authprovider': 'static',
 'authrole': 'anonymous',
 'session': 3463278813717336,
 'transport': {'peer': 'tcp4:127.0.0.1:21310',
               'protocol': 'wamp.2.msgpack',
               'type': 'rawsocket'}}

2019-11-25T15:38:28+0100 [Container   15270] >>>>>> MONITOR : session stats
{'authid': 'MTHR-ANE9-CFAR-6U4C-SV3M-X5AL',
 'authrole': 'anonymous',
 'realm': 'realm1',
 'session': 3463278813717336}
{'bytes': 1436,
 'cycle': 1,
 'duration': 57639160989,
 'first': True,
 'last': False,
 'messages': 2,
 'rated_messages': 4,
 'serializer': 'msgpack',
 'timestamp': 1574692651201417270}

2019-11-25T15:38:30+0100 [Container   15270] >>>>>> MONITOR : session stats
{'authid': 'MTHR-ANE9-CFAR-6U4C-SV3M-X5AL',
 'authrole': 'anonymous',
 'realm': 'realm1',
 'session': 3463278813717336}
{'bytes': 267,
 'cycle': 2,
 'duration': 2007641348,
 'first': False,
 'last': False,
 'messages': 10,
 'rated_messages': 10,
 'serializer': 'msgpack',
 'timestamp': 1574692708840580088}

2019-11-25T15:38:33+0100 [Router      15259] Router.detach(session=3463278813717336)
2019-11-25T15:38:33+0100 [Router      15259] Router.detach(session=3463278813717336): detached sessions [3463278813717336] from router realm "realm1"
2019-11-25T15:38:33+0100 [Container   15270] >>>>>> MONITOR : session 3463278813717336 left
2019-11-25T15:38:33+0100 [Container   15270] >>>>>> MONITOR : session stats
{'authid': 'MTHR-ANE9-CFAR-6U4C-SV3M-X5AL',
 'authrole': 'anonymous',
 'realm': 'realm1',
 'session': None}
{'bytes': 235,
 'cycle': 3,
 'duration': 3010591398,
 'first': False,
 'last': True,
 'messages': 9,
 'rated_messages': 9,
 'serializer': 'msgpack',
 'timestamp': 1574692710848236099}
```
