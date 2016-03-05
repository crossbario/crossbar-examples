# Call Roundtrip Time

This example measures WAMP remote call roundtrip time.

* A container worker is started with a single component that registers a procedure.
* A second container worker is started which calls the former procedure, waits for the result, and repeats.
* The time to perform N calls is measured, and the average round-trip time per call is computed.

Note that this does NOT measure throughput, as the calls are issued sequentially.

To test the influence of the WAMP transport, actually 4 container workers are started:

* the first pair of caller/callee container workers are using WAMP over Unix domain socket with RawSocket framing in MessagePack serialization
* the second pair of caller/callee container workers are using WAMP over loopback TCP with WebSocket framing in JSON serialization

Results:

* WAMP over Unix domain socket with RawSocket/MessagePack has an average RTT of 400 us
* WAMP over loopback TCP with WebSocket/JSON has an average RTT of 1.2 ms


## Crossbar.io Logs

```console
oberstet@bvr-sql18:~/scm/tavendo/crossbarexamples/benchmark/rpc_roundtrip$ /opt/crossbar/bin/crossbar start
2016-02-11T14:22:29+0100 [Controller  30212] Automatically choosing optimal Twisted reactor
2016-02-11T14:22:29+0100 [Controller  30212] Running on Linux and optimal reactor (epoll) was installed.
2016-02-11T14:22:30+0100 [Controller  30212]      __  __  __  __  __  __      __     __
2016-02-11T14:22:30+0100 [Controller  30212]     /  `|__)/  \/__`/__`|__) /\ |__)  |/  \
2016-02-11T14:22:30+0100 [Controller  30212]     \__,|  \\__/.__/.__/|__)/~~\|  \. |\__/
2016-02-11T14:22:30+0100 [Controller  30212]
2016-02-11T14:22:30+0100 [Controller  30212]     Crossbar.io Version: 0.12.1
2016-02-11T14:22:30+0100 [Controller  30212]     Node Public Key: f62b5a9732e279bd43d7ee39acc2f0111934066387e8d4ab3c7196583017fae4
2016-02-11T14:22:30+0100 [Controller  30212]
2016-02-11T14:22:30+0100 [Controller  30212] Running from node directory '/home/oberstet/scm/tavendo/crossbarexamples/benchmark/rpc_roundtrip/.crossbar'
2016-02-11T14:22:30+0100 [Controller  30212] Controller process starting (PyPy-EPollReactor) ..
2016-02-11T14:22:30+0100 [Controller  30212] Node configuration loaded from 'config.json'
2016-02-11T14:22:30+0100 [Controller  30212] Node ID 'bvr-sql18' set from hostname
2016-02-11T14:22:30+0100 [Controller  30212] Using default node shutdown triggers [u'shutdown_on_worker_exit']
2016-02-11T14:22:30+0100 [Controller  30212] Joined realm 'crossbar' on node management router
2016-02-11T14:22:30+0100 [Controller  30212] Starting Router with ID 'worker1'...
2016-02-11T14:22:31+0100 [Router      30220] Worker process starting (PyPy-EPollReactor) ..
2016-02-11T14:22:32+0100 [Controller  30212] Router with ID 'worker1' and PID 30220 started
2016-02-11T14:22:32+0100 [Router      30220] Realm 'realm1' started
2016-02-11T14:22:32+0100 [Controller  30212] Router 'worker1': realm 'realm1' (named 'realm1') started
2016-02-11T14:22:32+0100 [Controller  30212] Router 'worker1': role 'role1' (named 'anonymous') started on realm 'realm1'
2016-02-11T14:22:32+0100 [Router      30220] WampWebSocketServerFactory starting on 9000
2016-02-11T14:22:32+0100 [Controller  30212] Router 'worker1': transport 'transport1' started
2016-02-11T14:22:32+0100 [Router      30220] WampRawSocketServerFactory starting on '/home/oberstet/scm/tavendo/crossbarexamples/benchmark/rpc_roundtrip/.crossbar/crossbar.sock'
2016-02-11T14:22:32+0100 [Controller  30212] Router 'worker1': transport 'transport2' started
2016-02-11T14:22:32+0100 [Controller  30212] Starting Container with ID 'worker2'...
2016-02-11T14:22:32+0100 [Container   30226] Worker process starting (PyPy-EPollReactor) ..
2016-02-11T14:22:33+0100 [Controller  30212] Container with ID 'worker2' and PID 30226 started
2016-02-11T14:22:33+0100 [Controller  30212] Container 'worker2': component 'component1' started
2016-02-11T14:22:33+0100 [Controller  30212] Starting Container with ID 'worker3'...
2016-02-11T14:22:33+0100 [Container   30226] Ready!
2016-02-11T14:22:34+0100 [Container   30234] Worker process starting (PyPy-EPollReactor) ..
2016-02-11T14:22:35+0100 [Controller  30212] Container with ID 'worker3' and PID 30234 started
2016-02-11T14:22:35+0100 [Controller  30212] Container 'worker3': component 'component1' started
2016-02-11T14:22:35+0100 [Controller  30212] Starting Container with ID 'worker4'...
2016-02-11T14:22:36+0100 [Container   30242] Worker process starting (PyPy-EPollReactor) ..
2016-02-11T14:22:37+0100 [Controller  30212] Container with ID 'worker4' and PID 30242 started
2016-02-11T14:22:37+0100 [Controller  30212] Container 'worker4': component 'component1' started
2016-02-11T14:22:37+0100 [Controller  30212] Starting Container with ID 'worker5'...
2016-02-11T14:22:37+0100 [Container   30242] Ready!
2016-02-11T14:22:38+0100 [Container   30250] Worker process starting (PyPy-EPollReactor) ..
2016-02-11T14:22:38+0100 [Controller  30212] Container with ID 'worker5' and PID 30250 started
2016-02-11T14:22:38+0100 [Controller  30212] Container 'worker5': component 'component1' started
2016-02-11T14:22:40+0100 [Container   30234] [WAMP-UDS-RawSocket-MessagePack] - average round-trip time (ms): 4.80579018593
2016-02-11T14:22:42+0100 [Container   30234] [WAMP-UDS-RawSocket-MessagePack] - average round-trip time (ms): 2.43633794785
2016-02-11T14:22:43+0100 [Container   30234] [WAMP-UDS-RawSocket-MessagePack] - average round-trip time (ms): 1.07937598228
2016-02-11T14:22:44+0100 [Container   30234] [WAMP-UDS-RawSocket-MessagePack] - average round-trip time (ms): 0.81183886528
2016-02-11T14:22:44+0100 [Container   30234] [WAMP-UDS-RawSocket-MessagePack] - average round-trip time (ms): 0.405555009842
2016-02-11T14:22:45+0100 [Container   30234] [WAMP-UDS-RawSocket-MessagePack] - average round-trip time (ms): 0.427790164948
2016-02-11T14:22:45+0100 [Container   30234] [WAMP-UDS-RawSocket-MessagePack] - average round-trip time (ms): 0.441895008087
2016-02-11T14:22:46+0100 [Container   30234] [WAMP-UDS-RawSocket-MessagePack] - average round-trip time (ms): 0.353103876114
2016-02-11T14:22:46+0100 [Container   30250] [WAMP-TCP-WebSocket-JSON] - average round-trip time (ms): 7.28738903999
2016-02-11T14:22:46+0100 [Container   30234] [WAMP-UDS-RawSocket-MessagePack] - average round-trip time (ms): 0.329288005829
2016-02-11T14:22:46+0100 [Container   30234] [WAMP-UDS-RawSocket-MessagePack] - average round-trip time (ms): 0.398420095444
2016-02-11T14:22:47+0100 [Container   30234] [WAMP-UDS-RawSocket-MessagePack] - average round-trip time (ms): 0.412348985672
2016-02-11T14:22:47+0100 [Container   30234] [WAMP-UDS-RawSocket-MessagePack] - average round-trip time (ms): 0.477908849716
2016-02-11T14:22:48+0100 [Container   30234] [WAMP-UDS-RawSocket-MessagePack] - average round-trip time (ms): 0.38994717598
2016-02-11T14:22:48+0100 [Container   30234] [WAMP-UDS-RawSocket-MessagePack] - average round-trip time (ms): 0.314651012421
2016-02-11T14:22:48+0100 [Container   30234] [WAMP-UDS-RawSocket-MessagePack] - average round-trip time (ms): 0.373070001602
2016-02-11T14:22:49+0100 [Container   30234] [WAMP-UDS-RawSocket-MessagePack] - average round-trip time (ms): 0.354159832001
2016-02-11T14:22:49+0100 [Container   30234] [WAMP-UDS-RawSocket-MessagePack] - average round-trip time (ms): 0.374258995056
2016-02-11T14:22:49+0100 [Container   30250] [WAMP-TCP-WebSocket-JSON] - average round-trip time (ms): 3.43346405029
2016-02-11T14:22:49+0100 [Container   30234] [WAMP-UDS-RawSocket-MessagePack] - average round-trip time (ms): 0.409793138504
2016-02-11T14:22:50+0100 [Container   30234] [WAMP-UDS-RawSocket-MessagePack] - average round-trip time (ms): 0.350640058517
2016-02-11T14:22:50+0100 [Container   30234] [WAMP-UDS-RawSocket-MessagePack] - average round-trip time (ms): 0.374665975571
2016-02-11T14:22:51+0100 [Container   30234] [WAMP-UDS-RawSocket-MessagePack] - average round-trip time (ms): 0.373152971268
2016-02-11T14:22:51+0100 [Container   30234] [WAMP-UDS-RawSocket-MessagePack] - average round-trip time (ms): 0.345523834229
2016-02-11T14:22:51+0100 [Container   30234] [WAMP-UDS-RawSocket-MessagePack] - average round-trip time (ms): 0.393088102341
2016-02-11T14:22:51+0100 [Container   30250] [WAMP-TCP-WebSocket-JSON] - average round-trip time (ms): 2.18725085258
2016-02-11T14:22:52+0100 [Container   30234] [WAMP-UDS-RawSocket-MessagePack] - average round-trip time (ms): 0.327136039734
2016-02-11T14:22:52+0100 [Container   30234] [WAMP-UDS-RawSocket-MessagePack] - average round-trip time (ms): 0.340734004974
2016-02-11T14:22:52+0100 [Container   30234] [WAMP-UDS-RawSocket-MessagePack] - average round-trip time (ms): 0.372407913208
2016-02-11T14:22:53+0100 [Container   30234] [WAMP-UDS-RawSocket-MessagePack] - average round-trip time (ms): 0.347455978394
2016-02-11T14:22:53+0100 [Container   30250] [WAMP-TCP-WebSocket-JSON] - average round-trip time (ms): 1.57743000984
2016-02-11T14:22:53+0100 [Container   30234] [WAMP-UDS-RawSocket-MessagePack] - average round-trip time (ms): 0.370494127274
2016-02-11T14:22:53+0100 [Container   30234] [WAMP-UDS-RawSocket-MessagePack] - average round-trip time (ms): 0.374666929245
2016-02-11T14:22:54+0100 [Container   30234] [WAMP-UDS-RawSocket-MessagePack] - average round-trip time (ms): 0.359820127487
2016-02-11T14:22:54+0100 [Container   30234] [WAMP-UDS-RawSocket-MessagePack] - average round-trip time (ms): 0.386512994766
2016-02-11T14:22:54+0100 [Container   30250] [WAMP-TCP-WebSocket-JSON] - average round-trip time (ms): 1.32322597504
2016-02-11T14:22:55+0100 [Container   30234] [WAMP-UDS-RawSocket-MessagePack] - average round-trip time (ms): 0.376044988632
2016-02-11T14:22:55+0100 [Container   30234] [WAMP-UDS-RawSocket-MessagePack] - average round-trip time (ms): 0.332526922226
2016-02-11T14:22:55+0100 [Container   30234] [WAMP-UDS-RawSocket-MessagePack] - average round-trip time (ms): 0.373719930649
2016-02-11T14:22:56+0100 [Container   30250] [WAMP-TCP-WebSocket-JSON] - average round-trip time (ms): 1.29667520523
2016-02-11T14:22:56+0100 [Container   30234] [WAMP-UDS-RawSocket-MessagePack] - average round-trip time (ms): 0.384307146072
2016-02-11T14:22:56+0100 [Container   30234] [WAMP-UDS-RawSocket-MessagePack] - average round-trip time (ms): 0.478227853775
2016-02-11T14:22:56+0100 [Container   30234] [WAMP-UDS-RawSocket-MessagePack] - average round-trip time (ms): 0.382285118103
2016-02-11T14:22:57+0100 [Container   30250] [WAMP-TCP-WebSocket-JSON] - average round-trip time (ms): 1.20217490196
2016-02-11T14:22:57+0100 [Container   30234] [WAMP-UDS-RawSocket-MessagePack] - average round-trip time (ms): 0.369907855988
2016-02-11T14:22:57+0100 [Container   30234] [WAMP-UDS-RawSocket-MessagePack] - average round-trip time (ms): 0.379719018936
2016-02-11T14:22:58+0100 [Container   30234] [WAMP-UDS-RawSocket-MessagePack] - average round-trip time (ms): 0.382742166519
2016-02-11T14:22:58+0100 [Container   30234] [WAMP-UDS-RawSocket-MessagePack] - average round-trip time (ms): 0.365622997284
2016-02-11T14:22:58+0100 [Container   30250] [WAMP-TCP-WebSocket-JSON] - average round-trip time (ms): 1.27480602264
2016-02-11T14:22:58+0100 [Container   30234] [WAMP-UDS-RawSocket-MessagePack] - average round-trip time (ms): 0.380940914154
2016-02-11T14:22:59+0100 [Container   30234] [WAMP-UDS-RawSocket-MessagePack] - average round-trip time (ms): 0.346703052521
2016-02-11T14:22:59+0100 [Container   30234] [WAMP-UDS-RawSocket-MessagePack] - average round-trip time (ms): 0.427990913391
2016-02-11T14:22:59+0100 [Container   30250] [WAMP-TCP-WebSocket-JSON] - average round-trip time (ms): 1.30521392822
2016-02-11T14:23:00+0100 [Container   30234] [WAMP-UDS-RawSocket-MessagePack] - average round-trip time (ms): 0.400156974792
2016-02-11T14:23:00+0100 [Container   30234] [WAMP-UDS-RawSocket-MessagePack] - average round-trip time (ms): 0.379863023758
2016-02-11T14:23:00+0100 [Container   30234] [WAMP-UDS-RawSocket-MessagePack] - average round-trip time (ms): 0.418065071106
2016-02-11T14:23:00+0100 [Container   30250] [WAMP-TCP-WebSocket-JSON] - average round-trip time (ms): 1.19690608978
2016-02-11T14:23:01+0100 [Container   30234] [WAMP-UDS-RawSocket-MessagePack] - average round-trip time (ms): 0.357007980347
2016-02-11T14:23:01+0100 [Container   30234] [WAMP-UDS-RawSocket-MessagePack] - average round-trip time (ms): 0.38480591774
2016-02-11T14:23:01+0100 [Container   30234] [WAMP-UDS-RawSocket-MessagePack] - average round-trip time (ms): 0.398633956909
2016-02-11T14:23:02+0100 [Container   30250] [WAMP-TCP-WebSocket-JSON] - average round-trip time (ms): 1.28169989586
2016-02-11T14:23:02+0100 [Container   30234] [WAMP-UDS-RawSocket-MessagePack] - average round-trip time (ms): 0.37703204155
^C2016-02-11T14:23:02+0100 [Controller  30212] Received SIGINT, shutting down.
2016-02-11T14:23:02+0100 [Controller  30212] sending TERM to subprocess 30220
2016-02-11T14:23:02+0100 [Controller  30212] waiting for 30220 to exit...
2016-02-11T14:23:02+0100 [Controller  30212] sending TERM to subprocess 30226
2016-02-11T14:23:02+0100 [Controller  30212] waiting for 30226 to exit...
2016-02-11T14:23:02+0100 [Controller  30212] sending TERM to subprocess 30234
2016-02-11T14:23:02+0100 [Controller  30212] waiting for 30234 to exit...
2016-02-11T14:23:02+0100 [Controller  30212] sending TERM to subprocess 30242
2016-02-11T14:23:02+0100 [Controller  30212] waiting for 30242 to exit...
2016-02-11T14:23:02+0100 [Controller  30212] sending TERM to subprocess 30250
2016-02-11T14:23:02+0100 [Controller  30212] waiting for 30250 to exit...
2016-02-11T14:23:02+0100 [Container   30242] Native worker received SIGTERM - shutting down ..
2016-02-11T14:23:02+0100 [Container   30242] Shutdown of worker requested!
2016-02-11T14:23:02+0100 [Container   30250] Native worker received SIGTERM - shutting down ..
2016-02-11T14:23:02+0100 [Container   30250] Shutdown of worker requested!
2016-02-11T14:23:02+0100 [Router      30220] Native worker received SIGTERM - shutting down ..
2016-02-11T14:23:02+0100 [Router      30220] Shutdown of worker requested!
2016-02-11T14:23:02+0100 [Container   30226] Native worker received SIGTERM - shutting down ..
2016-02-11T14:23:02+0100 [Container   30226] Shutdown of worker requested!
2016-02-11T14:23:02+0100 [Container   30234] Native worker received SIGTERM - shutting down ..
2016-02-11T14:23:02+0100 [Container   30234] Shutdown of worker requested!
2016-02-11T14:23:02+0100 [Container   30226] Connection to node controller closed cleanly
2016-02-11T14:23:02+0100 [Router      30220] Connection to node controller closed cleanly
2016-02-11T14:23:02+0100 [Router      30220] (TCP Port 9000 Closed)
2016-02-11T14:23:02+0100 [Router      30220] (UNIX Port /home/oberstet/scm/tavendo/crossbarexamples/benchmark/rpc_roundtrip/.crossbar/crossbar.sock Closed)
2016-02-11T14:23:02+0100 [Container   30242] Connection to node controller closed cleanly
2016-02-11T14:23:02+0100 [Container   30234] Connection to node controller closed cleanly
2016-02-11T14:23:02+0100 [Container   30242] Lost connection to component 'component1' with code '1006'.
2016-02-11T14:23:02+0100 [Container   30242] connection was closed uncleanly (peer dropped the TCP connection without previous WebSocket closing handshake)
2016-02-11T14:23:02+0100 [Container   30242] Container is hosting no more components: shutting down.
2016-02-11T14:23:02+0100 [Container   30250] Connection to node controller closed cleanly
2016-02-11T14:23:02+0100 [Container   30250] Lost connection to component 'component1' with code '1006'.
2016-02-11T14:23:02+0100 [Container   30250] connection was closed uncleanly (peer dropped the TCP connection without previous WebSocket closing handshake)
2016-02-11T14:23:02+0100 [Container   30250] Container is hosting no more components: shutting down.
2016-02-11T14:23:02+0100 [Controller  30212] Native worker connection closed cleanly.
2016-02-11T14:23:02+0100 [Controller  30212] Node worker worker3 ended successfully
2016-02-11T14:23:02+0100 [Controller  30212] Node worker ended, and trigger 'shutdown_on_worker_exit' active
2016-02-11T14:23:02+0100 [Controller  30212] Node shutting down ..
2016-02-11T14:23:02+0100 [Controller  30212] Shutting down node...
2016-02-11T14:23:02+0100 [Controller  30212] Native worker connection closed cleanly.
2016-02-11T14:23:02+0100 [Controller  30212] Node worker worker2 ended successfully
2016-02-11T14:23:02+0100 [Controller  30212] Node worker ended, and trigger 'shutdown_on_worker_exit' active
2016-02-11T14:23:02+0100 [Controller  30212] Node is already shutting down.
2016-02-11T14:23:02+0100 [Controller  30212] Native worker connection closed cleanly.
2016-02-11T14:23:02+0100 [Controller  30212] Node worker worker4 ended successfully
2016-02-11T14:23:02+0100 [Controller  30212] Node worker ended, and trigger 'shutdown_on_worker_exit' active
2016-02-11T14:23:02+0100 [Controller  30212] Node is already shutting down.
2016-02-11T14:23:02+0100 [Controller  30212] Native worker connection closed cleanly.
2016-02-11T14:23:02+0100 [Controller  30212] Node worker worker1 ended successfully
2016-02-11T14:23:02+0100 [Controller  30212] Node worker ended, and trigger 'shutdown_on_worker_exit' active
2016-02-11T14:23:02+0100 [Controller  30212] Node is already shutting down.
2016-02-11T14:23:02+0100 [Controller  30212] Native worker connection closed cleanly.
2016-02-11T14:23:02+0100 [Controller  30212] Node worker worker5 ended successfully
2016-02-11T14:23:02+0100 [Controller  30212] Node worker ended, and trigger 'shutdown_on_worker_exit' active
2016-02-11T14:23:02+0100 [Controller  30212] Node is already shutting down.
oberstet@bvr-sql18:~/scm/tavendo/crossbarexamples/benchmark/rpc_roundtrip$ ^C
```

## System Load

The following shows the system load produced by the test.

```console
XXXXXXXX (debian jessie/sid 64bit / Linux 3.19.0-47-generic)                                           Uptime: 21 days, 21:59:01

CPU  [|              4.6%]   CPU       4.6%  nice:     0.0%   MEM      2.6%  active:    1.70T   SWAP      0.1%   LOAD    48-core
MEM  [               2.6%]   user:     3.7%  irq:      0.0%   total:  2.95T  inactive:  1.19T   total:   74.4G   1 min:    1.99
SWAP [               0.1%]   system:   0.9%  iowait:   0.0%   used:   78.2G  buffers:    457M   used:     107M   5 min:    1.40
                             idle:    95.3%  steal:    0.0%   free:   2.88T  cached:    2.87T   free:    74.3G   15 min:   1.11

NETWORK     Rx/s   Tx/s   TASKS 910 (968 thr), 3 run, 907 slp, 0 oth sorted automatically by cpu_percent, flat view
eth0        20Kb  586Kb
eth1          0b     0b     CPU%  MEM%  VIRT   RES   PID USER        NI S     TIME+ IOR/s IOW/s Command
lo        2.67Mb 2.67Mb     62.5   0.0  274M  220M 26707 oberstet     0 R   0:30.57     0     0 crossbar-worker [router]
p11p1         0b     0b     35.2   0.0     0     0   697 root        19 S 133h27:46     0     0 kipmi0
p11p2         0b     0b     34.0   0.0  275M  221M 26735 oberstet     0 S   0:17.66     0     0 crossbar-worker [container]
                            33.1   0.0  273M  219M 26728 oberstet     0 R   0:18.70     0     0 crossbar-worker [container]
DISK I/O     R/s    W/s     30.5   0.0  268M  214M 26700 oberstet     0 S   0:14.51     0     0 crossbar-controller
md0            0      0     24.2   0.0  261M  207M 26721 oberstet     0 S   0:14.62     0     0 crossbar-worker [container]
md1            0      0     21.3   0.0  262M  208M 26714 oberstet     0 S   0:13.29     0     0 crossbar-worker [container]
```

