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

* WAMP over Unix domain socket with RawSocket/MessagePack has an average RTT of 600 us
* WAMP over loopback TCP with WebSocket/JSON has an average RTT of 1.2 ms


## Crossbar.io Logs

```console
oberstet@bvr-sql18:~/scm/tavendo/crossbarexamples/benchmark/rpc_roundtrip$ /opt/crossbar/bin/crossbar start
2016-02-11T14:00:12+0100 [Controller  26700] Automatically choosing optimal Twisted reactor
2016-02-11T14:00:13+0100 [Controller  26700] Running on Linux and optimal reactor (epoll) was installed.
2016-02-11T14:00:13+0100 [Controller  26700]      __  __  __  __  __  __      __     __
2016-02-11T14:00:13+0100 [Controller  26700]     /  `|__)/  \/__`/__`|__) /\ |__)  |/  \
2016-02-11T14:00:13+0100 [Controller  26700]     \__,|  \\__/.__/.__/|__)/~~\|  \. |\__/
2016-02-11T14:00:13+0100 [Controller  26700]
2016-02-11T14:00:13+0100 [Controller  26700]     Crossbar.io Version: 0.12.1
2016-02-11T14:00:13+0100 [Controller  26700]     Node Public Key: f62b5a9732e279bd43d7ee39acc2f0111934066387e8d4ab3c7196583017fae4
2016-02-11T14:00:13+0100 [Controller  26700]
2016-02-11T14:00:13+0100 [Controller  26700] Running from node directory '/home/oberstet/scm/tavendo/crossbarexamples/benchmark/rp                                                                             c_roundtrip/.crossbar'
2016-02-11T14:00:13+0100 [Controller  26700] Controller process starting (PyPy-EPollReactor) ..
2016-02-11T14:00:13+0100 [Controller  26700] Node configuration loaded from 'config.json'
2016-02-11T14:00:13+0100 [Controller  26700] Node ID 'bvr-sql18' set from hostname
2016-02-11T14:00:13+0100 [Controller  26700] Using default node shutdown triggers [u'shutdown_on_worker_exit']
2016-02-11T14:00:13+0100 [Controller  26700] Joined realm 'crossbar' on node management router
2016-02-11T14:00:13+0100 [Controller  26700] Starting Router with ID 'worker1'...
2016-02-11T14:00:14+0100 [Router      26707] Worker process starting (PyPy-EPollReactor) ..
2016-02-11T14:00:15+0100 [Controller  26700] Router with ID 'worker1' and PID 26707 started
2016-02-11T14:00:15+0100 [Router      26707] Realm 'realm1' started
2016-02-11T14:00:15+0100 [Controller  26700] Router 'worker1': realm 'realm1' (named 'realm1') started
2016-02-11T14:00:15+0100 [Controller  26700] Router 'worker1': role 'role1' (named 'anonymous') started on realm 'realm1'
2016-02-11T14:00:15+0100 [Router      26707] WampWebSocketServerFactory starting on 9000
2016-02-11T14:00:15+0100 [Controller  26700] Router 'worker1': transport 'transport1' started
2016-02-11T14:00:15+0100 [Router      26707] WampRawSocketServerFactory starting on '/home/oberstet/scm/tavendo/crossbarexamples/b                                                                             enchmark/rpc_roundtrip/.crossbar/crossbar.sock'
2016-02-11T14:00:15+0100 [Controller  26700] Router 'worker1': transport 'transport2' started
2016-02-11T14:00:15+0100 [Controller  26700] Starting Container with ID 'worker2'...
2016-02-11T14:00:16+0100 [Container   26714] Worker process starting (PyPy-EPollReactor) ..
2016-02-11T14:00:17+0100 [Controller  26700] Container with ID 'worker2' and PID 26714 started
2016-02-11T14:00:17+0100 [Controller  26700] Container 'worker2': component 'component1' started
2016-02-11T14:00:17+0100 [Controller  26700] Starting Container with ID 'worker3'...
2016-02-11T14:00:17+0100 [Container   26714] Ready!
2016-02-11T14:00:17+0100 [Container   26721] Worker process starting (PyPy-EPollReactor) ..
2016-02-11T14:00:19+0100 [Controller  26700] Container with ID 'worker3' and PID 26721 started
2016-02-11T14:00:19+0100 [Controller  26700] Container 'worker3': component 'component1' started
2016-02-11T14:00:19+0100 [Controller  26700] Starting Container with ID 'worker4'...
2016-02-11T14:00:20+0100 [Container   26728] Worker process starting (PyPy-EPollReactor) ..
2016-02-11T14:00:20+0100 [Controller  26700] Container with ID 'worker4' and PID 26728 started
2016-02-11T14:00:20+0100 [Controller  26700] Container 'worker4': component 'component1' started
2016-02-11T14:00:20+0100 [Controller  26700] Starting Container with ID 'worker5'...
2016-02-11T14:00:20+0100 [Container   26728] Ready!
2016-02-11T14:00:21+0100 [Container   26735] Worker process starting (PyPy-EPollReactor) ..
2016-02-11T14:00:22+0100 [Controller  26700] Container with ID 'worker5' and PID 26735 started
2016-02-11T14:00:22+0100 [Controller  26700] Container 'worker5': component 'component1' started
2016-02-11T14:00:24+0100 [Container   26721] [WAMP-UDS-RawSocket-MessagePack] - average round-trip time (ms): 5.58165311813
2016-02-11T14:00:26+0100 [Container   26721] [WAMP-UDS-RawSocket-MessagePack] - average round-trip time (ms): 2.3040599823
2016-02-11T14:00:28+0100 [Container   26721] [WAMP-UDS-RawSocket-MessagePack] - average round-trip time (ms): 1.41247606277
2016-02-11T14:00:29+0100 [Container   26721] [WAMP-UDS-RawSocket-MessagePack] - average round-trip time (ms): 0.878462791443
2016-02-11T14:00:29+0100 [Container   26735] [WAMP-TCP-WebSocket-JSON] - average round-trip time (ms): 6.8927500248
2016-02-11T14:00:30+0100 [Container   26721] [WAMP-UDS-RawSocket-MessagePack] - average round-trip time (ms): 0.750791072845
2016-02-11T14:00:30+0100 [Container   26721] [WAMP-UDS-RawSocket-MessagePack] - average round-trip time (ms): 0.736382961273
2016-02-11T14:00:31+0100 [Container   26721] [WAMP-UDS-RawSocket-MessagePack] - average round-trip time (ms): 0.564650058746
2016-02-11T14:00:31+0100 [Container   26721] [WAMP-UDS-RawSocket-MessagePack] - average round-trip time (ms): 0.603157997131
2016-02-11T14:00:32+0100 [Container   26721] [WAMP-UDS-RawSocket-MessagePack] - average round-trip time (ms): 0.466041088104
2016-02-11T14:00:32+0100 [Container   26721] [WAMP-UDS-RawSocket-MessagePack] - average round-trip time (ms): 0.489506006241
2016-02-11T14:00:33+0100 [Container   26721] [WAMP-UDS-RawSocket-MessagePack] - average round-trip time (ms): 0.499768972397
2016-02-11T14:00:33+0100 [Container   26735] [WAMP-TCP-WebSocket-JSON] - average round-trip time (ms): 3.90689611435
2016-02-11T14:00:33+0100 [Container   26721] [WAMP-UDS-RawSocket-MessagePack] - average round-trip time (ms): 0.43411898613
2016-02-11T14:00:34+0100 [Container   26721] [WAMP-UDS-RawSocket-MessagePack] - average round-trip time (ms): 0.441419839859
2016-02-11T14:00:34+0100 [Container   26721] [WAMP-UDS-RawSocket-MessagePack] - average round-trip time (ms): 0.450133085251
2016-02-11T14:00:35+0100 [Container   26721] [WAMP-UDS-RawSocket-MessagePack] - average round-trip time (ms): 0.465315103531
2016-02-11T14:00:35+0100 [Container   26721] [WAMP-UDS-RawSocket-MessagePack] - average round-trip time (ms): 0.503415822983
2016-02-11T14:00:35+0100 [Container   26735] [WAMP-TCP-WebSocket-JSON] - average round-trip time (ms): 2.18496799469
2016-02-11T14:00:36+0100 [Container   26721] [WAMP-UDS-RawSocket-MessagePack] - average round-trip time (ms): 0.430277109146
2016-02-11T14:00:36+0100 [Container   26721] [WAMP-UDS-RawSocket-MessagePack] - average round-trip time (ms): 0.404797077179
2016-02-11T14:00:36+0100 [Container   26721] [WAMP-UDS-RawSocket-MessagePack] - average round-trip time (ms): 0.444624900818
2016-02-11T14:00:37+0100 [Container   26735] [WAMP-TCP-WebSocket-JSON] - average round-trip time (ms): 1.34276890755
2016-02-11T14:00:37+0100 [Container   26721] [WAMP-UDS-RawSocket-MessagePack] - average round-trip time (ms): 0.49370598793
2016-02-11T14:00:38+0100 [Container   26721] [WAMP-UDS-RawSocket-MessagePack] - average round-trip time (ms): 0.55331993103
2016-02-11T14:00:38+0100 [Container   26735] [WAMP-TCP-WebSocket-JSON] - average round-trip time (ms): 1.16049909592
2016-02-11T14:00:38+0100 [Container   26721] [WAMP-UDS-RawSocket-MessagePack] - average round-trip time (ms): 0.471898078918
2016-02-11T14:00:38+0100 [Container   26721] [WAMP-UDS-RawSocket-MessagePack] - average round-trip time (ms): 0.475480079651
2016-02-11T14:00:39+0100 [Container   26735] [WAMP-TCP-WebSocket-JSON] - average round-trip time (ms): 1.18601799011
2016-02-11T14:00:39+0100 [Container   26721] [WAMP-UDS-RawSocket-MessagePack] - average round-trip time (ms): 0.546914815903
2016-02-11T14:00:39+0100 [Container   26721] [WAMP-UDS-RawSocket-MessagePack] - average round-trip time (ms): 0.463078022003
2016-02-11T14:00:40+0100 [Container   26721] [WAMP-UDS-RawSocket-MessagePack] - average round-trip time (ms): 0.537131071091
2016-02-11T14:00:40+0100 [Container   26735] [WAMP-TCP-WebSocket-JSON] - average round-trip time (ms): 1.09175086021
2016-02-11T14:00:40+0100 [Container   26721] [WAMP-UDS-RawSocket-MessagePack] - average round-trip time (ms): 0.476305961609
2016-02-11T14:00:41+0100 [Container   26721] [WAMP-UDS-RawSocket-MessagePack] - average round-trip time (ms): 0.479513168335
2016-02-11T14:00:41+0100 [Container   26735] [WAMP-TCP-WebSocket-JSON] - average round-trip time (ms): 1.11547017097
2016-02-11T14:00:41+0100 [Container   26721] [WAMP-UDS-RawSocket-MessagePack] - average round-trip time (ms): 0.492719888687
2016-02-11T14:00:42+0100 [Container   26721] [WAMP-UDS-RawSocket-MessagePack] - average round-trip time (ms): 0.492496967316
2016-02-11T14:00:42+0100 [Container   26735] [WAMP-TCP-WebSocket-JSON] - average round-trip time (ms): 1.11476397514
2016-02-11T14:00:42+0100 [Container   26721] [WAMP-UDS-RawSocket-MessagePack] - average round-trip time (ms): 0.514586925507
2016-02-11T14:00:43+0100 [Container   26721] [WAMP-UDS-RawSocket-MessagePack] - average round-trip time (ms): 0.545044183731
2016-02-11T14:00:43+0100 [Container   26735] [WAMP-TCP-WebSocket-JSON] - average round-trip time (ms): 1.22380685806
2016-02-11T14:00:43+0100 [Container   26721] [WAMP-UDS-RawSocket-MessagePack] - average round-trip time (ms): 0.496349811554
2016-02-11T14:00:44+0100 [Container   26721] [WAMP-UDS-RawSocket-MessagePack] - average round-trip time (ms): 0.527788162231
2016-02-11T14:00:44+0100 [Container   26721] [WAMP-UDS-RawSocket-MessagePack] - average round-trip time (ms): 0.441773891449
2016-02-11T14:00:45+0100 [Container   26735] [WAMP-TCP-WebSocket-JSON] - average round-trip time (ms): 1.07458806038
2016-02-11T14:00:45+0100 [Container   26721] [WAMP-UDS-RawSocket-MessagePack] - average round-trip time (ms): 0.396943092346
2016-02-11T14:00:45+0100 [Container   26721] [WAMP-UDS-RawSocket-MessagePack] - average round-trip time (ms): 0.420019865036
2016-02-11T14:00:45+0100 [Container   26735] [WAMP-TCP-WebSocket-JSON] - average round-trip time (ms): 0.949306964874
2016-02-11T14:00:46+0100 [Container   26721] [WAMP-UDS-RawSocket-MessagePack] - average round-trip time (ms): 0.416629076004
2016-02-11T14:00:46+0100 [Container   26721] [WAMP-UDS-RawSocket-MessagePack] - average round-trip time (ms): 0.466844081879
2016-02-11T14:00:47+0100 [Container   26735] [WAMP-TCP-WebSocket-JSON] - average round-trip time (ms): 1.03293800354
2016-02-11T14:00:47+0100 [Container   26721] [WAMP-UDS-RawSocket-MessagePack] - average round-trip time (ms): 0.462059020996
2016-02-11T14:00:47+0100 [Container   26721] [WAMP-UDS-RawSocket-MessagePack] - average round-trip time (ms): 0.478240013123
2016-02-11T14:00:48+0100 [Container   26721] [WAMP-UDS-RawSocket-MessagePack] - average round-trip time (ms): 0.487049818039
2016-02-11T14:00:48+0100 [Container   26735] [WAMP-TCP-WebSocket-JSON] - average round-trip time (ms): 1.10293102264
2016-02-11T14:00:48+0100 [Container   26721] [WAMP-UDS-RawSocket-MessagePack] - average round-trip time (ms): 0.485652208328
2016-02-11T14:00:49+0100 [Container   26721] [WAMP-UDS-RawSocket-MessagePack] - average round-trip time (ms): 0.517254829407
2016-02-11T14:00:49+0100 [Container   26735] [WAMP-TCP-WebSocket-JSON] - average round-trip time (ms): 1.14689207077
2016-02-11T14:00:49+0100 [Container   26721] [WAMP-UDS-RawSocket-MessagePack] - average round-trip time (ms): 0.621169090271
2016-02-11T14:00:50+0100 [Container   26721] [WAMP-UDS-RawSocket-MessagePack] - average round-trip time (ms): 0.512310028076
2016-02-11T14:00:50+0100 [Container   26735] [WAMP-TCP-WebSocket-JSON] - average round-trip time (ms): 1.27061390877
2016-02-11T14:00:50+0100 [Container   26721] [WAMP-UDS-RawSocket-MessagePack] - average round-trip time (ms): 0.487911939621
2016-02-11T14:00:51+0100 [Container   26721] [WAMP-UDS-RawSocket-MessagePack] - average round-trip time (ms): 0.481225013733
2016-02-11T14:00:51+0100 [Container   26735] [WAMP-TCP-WebSocket-JSON] - average round-trip time (ms): 1.02909517288
2016-02-11T14:00:51+0100 [Container   26721] [WAMP-UDS-RawSocket-MessagePack] - average round-trip time (ms): 0.523982048035
2016-02-11T14:00:52+0100 [Container   26721] [WAMP-UDS-RawSocket-MessagePack] - average round-trip time (ms): 0.510256052017
2016-02-11T14:00:52+0100 [Container   26721] [WAMP-UDS-RawSocket-MessagePack] - average round-trip time (ms): 0.452259778976
2016-02-11T14:00:52+0100 [Container   26735] [WAMP-TCP-WebSocket-JSON] - average round-trip time (ms): 1.1883058548
2016-02-11T14:00:53+0100 [Container   26721] [WAMP-UDS-RawSocket-MessagePack] - average round-trip time (ms): 0.521782159805
2016-02-11T14:00:53+0100 [Container   26721] [WAMP-UDS-RawSocket-MessagePack] - average round-trip time (ms): 0.505028963089
2016-02-11T14:00:53+0100 [Container   26735] [WAMP-TCP-WebSocket-JSON] - average round-trip time (ms): 1.16333699226
2016-02-11T14:00:54+0100 [Container   26721] [WAMP-UDS-RawSocket-MessagePack] - average round-trip time (ms): 0.455795049667
2016-02-11T14:00:54+0100 [Container   26721] [WAMP-UDS-RawSocket-MessagePack] - average round-trip time (ms): 0.458721876144
2016-02-11T14:00:54+0100 [Container   26735] [WAMP-TCP-WebSocket-JSON] - average round-trip time (ms): 1.08811712265
2016-02-11T14:00:55+0100 [Container   26721] [WAMP-UDS-RawSocket-MessagePack] - average round-trip time (ms): 0.445448160172
2016-02-11T14:00:55+0100 [Container   26721] [WAMP-UDS-RawSocket-MessagePack] - average round-trip time (ms): 0.403711795807
2016-02-11T14:00:55+0100 [Container   26721] [WAMP-UDS-RawSocket-MessagePack] - average round-trip time (ms): 0.420506000519
2016-02-11T14:00:55+0100 [Container   26735] [WAMP-TCP-WebSocket-JSON] - average round-trip time (ms): 0.946876049042
2016-02-11T14:00:56+0100 [Container   26721] [WAMP-UDS-RawSocket-MessagePack] - average round-trip time (ms): 0.436464071274
2016-02-11T14:00:56+0100 [Container   26721] [WAMP-UDS-RawSocket-MessagePack] - average round-trip time (ms): 0.512340068817
2016-02-11T14:00:57+0100 [Container   26735] [WAMP-TCP-WebSocket-JSON] - average round-trip time (ms): 1.06168293953
2016-02-11T14:00:57+0100 [Container   26721] [WAMP-UDS-RawSocket-MessagePack] - average round-trip time (ms): 0.496940851212
2016-02-11T14:00:57+0100 [Container   26721] [WAMP-UDS-RawSocket-MessagePack] - average round-trip time (ms): 0.473771095276
2016-02-11T14:00:58+0100 [Container   26735] [WAMP-TCP-WebSocket-JSON] - average round-trip time (ms): 1.10799789429
2016-02-11T14:00:58+0100 [Container   26721] [WAMP-UDS-RawSocket-MessagePack] - average round-trip time (ms): 0.482969045639
2016-02-11T14:00:58+0100 [Container   26721] [WAMP-UDS-RawSocket-MessagePack] - average round-trip time (ms): 0.454550981522
2016-02-11T14:00:59+0100 [Container   26735] [WAMP-TCP-WebSocket-JSON] - average round-trip time (ms): 1.06947302818
2016-02-11T14:00:59+0100 [Container   26721] [WAMP-UDS-RawSocket-MessagePack] - average round-trip time (ms): 0.473803043365
2016-02-11T14:00:59+0100 [Container   26721] [WAMP-UDS-RawSocket-MessagePack] - average round-trip time (ms): 0.746989011765
2016-02-11T14:01:00+0100 [Container   26735] [WAMP-TCP-WebSocket-JSON] - average round-trip time (ms): 1.16575908661
2016-02-11T14:01:00+0100 [Container   26721] [WAMP-UDS-RawSocket-MessagePack] - average round-trip time (ms): 0.500150918961
2016-02-11T14:01:00+0100 [Container   26721] [WAMP-UDS-RawSocket-MessagePack] - average round-trip time (ms): 0.518331050873
2016-02-11T14:01:01+0100 [Container   26721] [WAMP-UDS-RawSocket-MessagePack] - average round-trip time (ms): 0.563124895096
2016-02-11T14:01:01+0100 [Container   26735] [WAMP-TCP-WebSocket-JSON] - average round-trip time (ms): 1.23156189919
2016-02-11T14:01:02+0100 [Container   26721] [WAMP-UDS-RawSocket-MessagePack] - average round-trip time (ms): 0.479174137115
2016-02-11T14:01:02+0100 [Container   26721] [WAMP-UDS-RawSocket-MessagePack] - average round-trip time (ms): 0.516654014587
2016-02-11T14:01:02+0100 [Container   26735] [WAMP-TCP-WebSocket-JSON] - average round-trip time (ms): 1.14084506035
2016-02-11T14:01:03+0100 [Container   26721] [WAMP-UDS-RawSocket-MessagePack] - average round-trip time (ms): 0.50630402565
2016-02-11T14:01:03+0100 [Container   26721] [WAMP-UDS-RawSocket-MessagePack] - average round-trip time (ms): 0.523569822311
2016-02-11T14:01:04+0100 [Container   26735] [WAMP-TCP-WebSocket-JSON] - average round-trip time (ms): 1.2958240509
2016-02-11T14:01:04+0100 [Container   26721] [WAMP-UDS-RawSocket-MessagePack] - average round-trip time (ms): 0.466562986374
2016-02-11T14:01:04+0100 [Container   26721] [WAMP-UDS-RawSocket-MessagePack] - average round-trip time (ms): 0.491366147995
2016-02-11T14:01:05+0100 [Container   26721] [WAMP-UDS-RawSocket-MessagePack] - average round-trip time (ms): 0.525665998459
2016-02-11T14:01:05+0100 [Container   26735] [WAMP-TCP-WebSocket-JSON] - average round-trip time (ms): 1.12604999542
2016-02-11T14:01:05+0100 [Container   26721] [WAMP-UDS-RawSocket-MessagePack] - average round-trip time (ms): 0.48955988884
2016-02-11T14:01:06+0100 [Container   26721] [WAMP-UDS-RawSocket-MessagePack] - average round-trip time (ms): 0.473951101303
2016-02-11T14:01:06+0100 [Container   26735] [WAMP-TCP-WebSocket-JSON] - average round-trip time (ms): 1.02337694168
2016-02-11T14:01:06+0100 [Container   26721] [WAMP-UDS-RawSocket-MessagePack] - average round-trip time (ms): 0.387964963913
2016-02-11T14:01:06+0100 [Container   26721] [WAMP-UDS-RawSocket-MessagePack] - average round-trip time (ms): 0.40970492363
2016-02-11T14:01:07+0100 [Container   26735] [WAMP-TCP-WebSocket-JSON] - average round-trip time (ms): 0.98551607132
2016-02-11T14:01:07+0100 [Container   26721] [WAMP-UDS-RawSocket-MessagePack] - average round-trip time (ms): 0.462218999863
2016-02-11T14:01:07+0100 [Container   26721] [WAMP-UDS-RawSocket-MessagePack] - average round-trip time (ms): 0.507702112198
2016-02-11T14:01:08+0100 [Container   26735] [WAMP-TCP-WebSocket-JSON] - average round-trip time (ms): 1.07593297958
2016-02-11T14:01:08+0100 [Container   26721] [WAMP-UDS-RawSocket-MessagePack] - average round-trip time (ms): 0.489716053009
2016-02-11T14:01:08+0100 [Container   26721] [WAMP-UDS-RawSocket-MessagePack] - average round-trip time (ms): 0.503151893616
2016-02-11T14:01:09+0100 [Container   26721] [WAMP-UDS-RawSocket-MessagePack] - average round-trip time (ms): 0.554393053055
2016-02-11T14:01:09+0100 [Container   26735] [WAMP-TCP-WebSocket-JSON] - average round-trip time (ms): 1.19511985779
2016-02-11T14:01:09+0100 [Container   26721] [WAMP-UDS-RawSocket-MessagePack] - average round-trip time (ms): 0.502527952194
2016-02-11T14:01:10+0100 [Container   26721] [WAMP-UDS-RawSocket-MessagePack] - average round-trip time (ms): 0.604379892349
2016-02-11T14:01:10+0100 [Container   26735] [WAMP-TCP-WebSocket-JSON] - average round-trip time (ms): 1.24047803879
2016-02-11T14:01:10+0100 [Container   26721] [WAMP-UDS-RawSocket-MessagePack] - average round-trip time (ms): 0.545567989349
2016-02-11T14:01:11+0100 [Container   26721] [WAMP-UDS-RawSocket-MessagePack] - average round-trip time (ms): 0.493972063065
2016-02-11T14:01:11+0100 [Container   26735] [WAMP-TCP-WebSocket-JSON] - average round-trip time (ms): 1.08354711533
2016-02-11T14:01:11+0100 [Container   26721] [WAMP-UDS-RawSocket-MessagePack] - average round-trip time (ms): 0.499305963516
2016-02-11T14:01:12+0100 [Container   26721] [WAMP-UDS-RawSocket-MessagePack] - average round-trip time (ms): 0.517296075821
2016-02-11T14:01:12+0100 [Container   26735] [WAMP-TCP-WebSocket-JSON] - average round-trip time (ms): 1.13585686684
2016-02-11T14:01:12+0100 [Container   26721] [WAMP-UDS-RawSocket-MessagePack] - average round-trip time (ms): 0.495909929276
2016-02-11T14:01:13+0100 [Container   26721] [WAMP-UDS-RawSocket-MessagePack] - average round-trip time (ms): 0.489399194717
2016-02-11T14:01:13+0100 [Container   26721] [WAMP-UDS-RawSocket-MessagePack] - average round-trip time (ms): 0.464252948761
2016-02-11T14:01:14+0100 [Container   26735] [WAMP-TCP-WebSocket-JSON] - average round-trip time (ms): 1.20428109169
2016-02-11T14:01:14+0100 [Container   26721] [WAMP-UDS-RawSocket-MessagePack] - average round-trip time (ms): 0.463536977768
2016-02-11T14:01:14+0100 [Container   26721] [WAMP-UDS-RawSocket-MessagePack] - average round-trip time (ms): 0.402819871902
2016-02-11T14:01:15+0100 [Container   26735] [WAMP-TCP-WebSocket-JSON] - average round-trip time (ms): 1.10676908493
2016-02-11T14:01:15+0100 [Container   26721] [WAMP-UDS-RawSocket-MessagePack] - average round-trip time (ms): 0.505769014359
2016-02-11T14:01:15+0100 [Container   26721] [WAMP-UDS-RawSocket-MessagePack] - average round-trip time (ms): 0.468873977661
2016-02-11T14:01:16+0100 [Container   26721] [WAMP-UDS-RawSocket-MessagePack] - average round-trip time (ms): 0.398880004883
2016-02-11T14:01:16+0100 [Container   26735] [WAMP-TCP-WebSocket-JSON] - average round-trip time (ms): 1.09207081795
2016-02-11T14:01:16+0100 [Container   26721] [WAMP-UDS-RawSocket-MessagePack] - average round-trip time (ms): 0.433965206146
2016-02-11T14:01:17+0100 [Container   26721] [WAMP-UDS-RawSocket-MessagePack] - average round-trip time (ms): 0.475842952728
2016-02-11T14:01:17+0100 [Container   26735] [WAMP-TCP-WebSocket-JSON] - average round-trip time (ms): 1.0352139473
2016-02-11T14:01:17+0100 [Container   26721] [WAMP-UDS-RawSocket-MessagePack] - average round-trip time (ms): 0.464903831482
2016-02-11T14:01:18+0100 [Container   26721] [WAMP-UDS-RawSocket-MessagePack] - average round-trip time (ms): 0.443825006485
2016-02-11T14:01:18+0100 [Container   26735] [WAMP-TCP-WebSocket-JSON] - average round-trip time (ms): 0.967012166977
2016-02-11T14:01:18+0100 [Container   26721] [WAMP-UDS-RawSocket-MessagePack] - average round-trip time (ms): 0.388709068298
2016-02-11T14:01:18+0100 [Container   26721] [WAMP-UDS-RawSocket-MessagePack] - average round-trip time (ms): 0.373323917389
2016-02-11T14:01:19+0100 [Container   26721] [WAMP-UDS-RawSocket-MessagePack] - average round-trip time (ms): 0.539892196655
2016-02-11T14:01:19+0100 [Container   26735] [WAMP-TCP-WebSocket-JSON] - average round-trip time (ms): 1.1410009861
2016-02-11T14:01:19+0100 [Container   26721] [WAMP-UDS-RawSocket-MessagePack] - average round-trip time (ms): 0.430224895477
2016-02-11T14:01:20+0100 [Container   26721] [WAMP-UDS-RawSocket-MessagePack] - average round-trip time (ms): 0.441931009293
2016-02-11T14:01:20+0100 [Container   26735] [WAMP-TCP-WebSocket-JSON] - average round-trip time (ms): 0.994971990585
2016-02-11T14:01:20+0100 [Container   26721] [WAMP-UDS-RawSocket-MessagePack] - average round-trip time (ms): 0.415280103683
2016-02-11T14:01:20+0100 [Container   26721] [WAMP-UDS-RawSocket-MessagePack] - average round-trip time (ms): 0.357184886932
2016-02-11T14:01:21+0100 [Container   26735] [WAMP-TCP-WebSocket-JSON] - average round-trip time (ms): 1.02566099167
2016-02-11T14:01:21+0100 [Container   26721] [WAMP-UDS-RawSocket-MessagePack] - average round-trip time (ms): 0.495332956314
2016-02-11T14:01:21+0100 [Container   26721] [WAMP-UDS-RawSocket-MessagePack] - average round-trip time (ms): 0.532006978989
^C2016-02-11T14:01:22+0100 [Controller  26700] Received SIGINT, shutting down.
2016-02-11T14:01:22+0100 [Controller  26700] sending TERM to subprocess 26707
2016-02-11T14:01:22+0100 [Controller  26700] waiting for 26707 to exit...
2016-02-11T14:01:22+0100 [Controller  26700] sending TERM to subprocess 26714
2016-02-11T14:01:22+0100 [Controller  26700] waiting for 26714 to exit...
2016-02-11T14:01:22+0100 [Controller  26700] sending TERM to subprocess 26721
2016-02-11T14:01:22+0100 [Controller  26700] waiting for 26721 to exit...
2016-02-11T14:01:22+0100 [Controller  26700] sending TERM to subprocess 26728
2016-02-11T14:01:22+0100 [Controller  26700] waiting for 26728 to exit...
2016-02-11T14:01:22+0100 [Controller  26700] sending TERM to subprocess 26735
2016-02-11T14:01:22+0100 [Controller  26700] waiting for 26735 to exit...
2016-02-11T14:01:22+0100 [Container   26728] Native worker received SIGTERM - shutting down ..
2016-02-11T14:01:22+0100 [Container   26728] Shutdown of worker requested!
2016-02-11T14:01:22+0100 [Container   26735] Native worker received SIGTERM - shutting down ..
2016-02-11T14:01:22+0100 [Container   26735] Shutdown of worker requested!
2016-02-11T14:01:22+0100 [Router      26707] Native worker received SIGTERM - shutting down ..
2016-02-11T14:01:22+0100 [Router      26707] Shutdown of worker requested!
2016-02-11T14:01:22+0100 [Container   26714] Native worker received SIGTERM - shutting down ..
2016-02-11T14:01:22+0100 [Container   26714] Shutdown of worker requested!
2016-02-11T14:01:22+0100 [Container   26721] Native worker received SIGTERM - shutting down ..
2016-02-11T14:01:22+0100 [Container   26721] Shutdown of worker requested!
2016-02-11T14:01:22+0100 [Container   26721] [WAMP-UDS-RawSocket-MessagePack] - average round-trip time (ms): 0.546066045761
2016-02-11T14:01:22+0100 [Container   26714] Connection to node controller closed cleanly
2016-02-11T14:01:22+0100 [Container   26721] Connection to node controller closed cleanly
2016-02-11T14:01:22+0100 [Container   26728] Connection to node controller closed cleanly
2016-02-11T14:01:22+0100 [Container   26735] Connection to node controller closed cleanly
2016-02-11T14:01:22+0100 [Container   26735] Lost connection to component 'component1' with code '1006'.
2016-02-11T14:01:22+0100 [Container   26735] connection was closed uncleanly (peer dropped the TCP connection without previous WebSocket closing handshake)
2016-02-11T14:01:22+0100 [Router      26707] Connection to node controller closed cleanly
2016-02-11T14:01:22+0100 [Router      26707] (TCP Port 9000 Closed)
2016-02-11T14:01:22+0100 [Router      26707] (UNIX Port /home/oberstet/scm/tavendo/crossbarexamples/benchmark/rpc_roundtrip/.crossbar/crossbar.sock Closed)
2016-02-11T14:01:22+0100 [Container   26728] Lost connection to component 'component1' with code '1006'.
2016-02-11T14:01:22+0100 [Container   26728] connection was closed uncleanly (peer dropped the TCP connection without previous WebSocket closing handshake)
2016-02-11T14:01:22+0100 [Container   26728] Container is hosting no more components: shutting down.
2016-02-11T14:01:22+0100 [Container   26735] Container is hosting no more components: shutting down.
2016-02-11T14:01:22+0100 [Controller  26700] Native worker connection closed cleanly.
2016-02-11T14:01:22+0100 [Controller  26700] Node worker worker2 ended successfully
2016-02-11T14:01:22+0100 [Controller  26700] Node worker ended, and trigger 'shutdown_on_worker_exit' active
2016-02-11T14:01:22+0100 [Controller  26700] Node shutting down ..
2016-02-11T14:01:22+0100 [Controller  26700] Shutting down node...
2016-02-11T14:01:22+0100 [Controller  26700] Native worker connection closed cleanly.
2016-02-11T14:01:22+0100 [Controller  26700] Node worker worker3 ended successfully
2016-02-11T14:01:22+0100 [Controller  26700] Node worker ended, and trigger 'shutdown_on_worker_exit' active
2016-02-11T14:01:22+0100 [Controller  26700] Node is already shutting down.
2016-02-11T14:01:22+0100 [Controller  26700] Native worker connection closed cleanly.
2016-02-11T14:01:22+0100 [Controller  26700] Node worker worker1 ended successfully
2016-02-11T14:01:22+0100 [Controller  26700] Node worker ended, and trigger 'shutdown_on_worker_exit' active
2016-02-11T14:01:22+0100 [Controller  26700] Node is already shutting down.
2016-02-11T14:01:22+0100 [Controller  26700] Native worker connection closed cleanly.
2016-02-11T14:01:22+0100 [Controller  26700] Node worker worker5 ended successfully
2016-02-11T14:01:22+0100 [Controller  26700] Node worker ended, and trigger 'shutdown_on_worker_exit' active
2016-02-11T14:01:22+0100 [Controller  26700] Node is already shutting down.
2016-02-11T14:01:22+0100 [Controller  26700] Native worker connection closed cleanly.
2016-02-11T14:01:22+0100 [Controller  26700] Node worker worker4 ended successfully
2016-02-11T14:01:22+0100 [Controller  26700] Node worker ended, and trigger 'shutdown_on_worker_exit' active
2016-02-11T14:01:22+0100 [Controller  26700] Node is already shutting down.
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

