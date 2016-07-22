# How it works

The `com.example.compute` procedure is registered by 2 microservice instances (processes).

The first one registers at a maximum concurrency of 2, while the latter at a maximum concurrency of 3.

So both microservices instances combined can handle a maximum concurrency of 5.

The implementation (callee side) of `com.example.compute` will just sleep (on a background thread) for 2 seconds.

The caller client will issue 20 calls to `com.example.compute`.

Now, 20 / 5 * 2 = 8, so we expect to wait 8s for everything to finish, which is what you can see in the caller log:

```console
2016-07-22T09:37:33+0200 total run-time (wallclock): 8.04397702217
```

# How to try

Open a first terminal and start Crossbar.io:

```
crossbar start
```

Open a second terminal and run the driving client:

```
python client.py
```

Here is log output for the first:

```console
(cpy2711_11) oberstet@thinkpad-t430s:~/scm/crossbario/crossbarexamples/concurrency-control/queued$ crossbar start
2016-07-22T09:37:20+0200 [Controller   3774]      __  __  __  __  __  __      __     __
2016-07-22T09:37:20+0200 [Controller   3774]     /  `|__)/  \/__`/__`|__) /\ |__)  |/  \
2016-07-22T09:37:20+0200 [Controller   3774]     \__,|  \\__/.__/.__/|__)/~~\|  \. |\__/
2016-07-22T09:37:20+0200 [Controller   3774]
2016-07-22T09:37:20+0200 [Controller   3774]     Crossbar.io Version: 0.15.0
2016-07-22T09:37:20+0200 [Controller   3774]     Node Public Key: ad5bf793a3ad2b7ef4c765228affbacf40574147f3bd484494359ce1440c0b59
2016-07-22T09:37:20+0200 [Controller   3774]
2016-07-22T09:37:20+0200 [Controller   3774] Running from node directory '/home/oberstet/scm/crossbario/crossbarexamples/concurrency-control/queued/.crossbar'
2016-07-22T09:37:20+0200 [Controller   3774] Controller process starting (CPython-EPollReactor) ..
2016-07-22T09:37:20+0200 [Controller   3774] Node configuration loaded from 'config.json'
2016-07-22T09:37:20+0200 [Controller   3774] Node ID 'thinkpad-t430s' set from hostname
2016-07-22T09:37:20+0200 [Controller   3774] Using default node shutdown triggers [u'shutdown_on_worker_exit']
2016-07-22T09:37:20+0200 [Controller   3774] Joined realm 'crossbar' on node management router
2016-07-22T09:37:20+0200 [Controller   3774] Starting Router with ID 'worker-001'...
2016-07-22T09:37:20+0200 [Router       3782] Worker process starting (CPython-EPollReactor) ..
2016-07-22T09:37:20+0200 [Controller   3774] Router with ID 'worker-001' and PID 3782 started
2016-07-22T09:37:20+0200 [Router       3782] Realm 'realm1' started
2016-07-22T09:37:20+0200 [Controller   3774] Router 'worker-001': realm 'realm-001' (named 'realm1') started
2016-07-22T09:37:20+0200 [Controller   3774] Router 'worker-001': role 'role-001' (named 'anonymous') started on realm 'realm-001'
2016-07-22T09:37:20+0200 [Router       3782] UniSocketServerFactory starting on 8080
2016-07-22T09:37:20+0200 [Controller   3774] Router 'worker-001': transport 'transport-001' started
2016-07-22T09:37:20+0200 [Controller   3774] Starting Container with ID 'worker-002'...
2016-07-22T09:37:20+0200 [Container    3787] Worker process starting (CPython-EPollReactor) ..
2016-07-22T09:37:21+0200 [Controller   3774] Container with ID 'worker-002' and PID 3787 started
2016-07-22T09:37:21+0200 [Controller   3774] Container 'worker-002': component 'component-001' started
2016-07-22T09:37:21+0200 [Controller   3774] Starting Container with ID 'worker-003'...
2016-07-22T09:37:21+0200 [Container    3787] ComputeKernel ready with concurrency 3!
2016-07-22T09:37:21+0200 [Container    3792] Worker process starting (CPython-EPollReactor) ..
2016-07-22T09:37:21+0200 [Controller   3774] Container with ID 'worker-003' and PID 3792 started
2016-07-22T09:37:21+0200 [Controller   3774] Container 'worker-003': component 'component-002' started
2016-07-22T09:37:21+0200 [Container    3792] ComputeKernel ready with concurrency 2!
2016-07-22T09:37:24+0200 [Container    3787] starting compute() on background thread (current concurrency 1 of max 3) ..
2016-07-22T09:37:24+0200 [Container    3792] starting compute() on background thread (current concurrency 1 of max 2) ..
2016-07-22T09:37:24+0200 [Container    3792] starting compute() on background thread (current concurrency 2 of max 2) ..
2016-07-22T09:37:24+0200 [Container    3787] starting compute() on background thread (current concurrency 2 of max 3) ..
2016-07-22T09:37:24+0200 [Container    3787] starting compute() on background thread (current concurrency 3 of max 3) ..
2016-07-22T09:37:26+0200 [Container    3787] compute() ended from background thread (3 invocations, current concurrency 2 of max 3)
2016-07-22T09:37:26+0200 [Container    3787] compute() ended from background thread (3 invocations, current concurrency 1 of max 3)
2016-07-22T09:37:26+0200 [Container    3792] compute() ended from background thread (2 invocations, current concurrency 1 of max 2)
2016-07-22T09:37:26+0200 [Container    3792] compute() ended from background thread (2 invocations, current concurrency 0 of max 2)
2016-07-22T09:37:26+0200 [Container    3792] starting compute() on background thread (current concurrency 1 of max 2) ..
2016-07-22T09:37:27+0200 [Container    3792] starting compute() on background thread (current concurrency 2 of max 2) ..
2016-07-22T09:37:27+0200 [Container    3787] compute() ended from background thread (3 invocations, current concurrency 0 of max 3)
2016-07-22T09:37:27+0200 [Container    3787] starting compute() on background thread (current concurrency 1 of max 3) ..
2016-07-22T09:37:27+0200 [Container    3787] starting compute() on background thread (current concurrency 2 of max 3) ..
2016-07-22T09:37:27+0200 [Container    3787] starting compute() on background thread (current concurrency 3 of max 3) ..
2016-07-22T09:37:29+0200 [Container    3792] compute() ended from background thread (4 invocations, current concurrency 1 of max 2)
2016-07-22T09:37:29+0200 [Container    3792] compute() ended from background thread (4 invocations, current concurrency 0 of max 2)
2016-07-22T09:37:29+0200 [Container    3787] compute() ended from background thread (6 invocations, current concurrency 2 of max 3)
2016-07-22T09:37:29+0200 [Container    3792] starting compute() on background thread (current concurrency 1 of max 2) ..
2016-07-22T09:37:29+0200 [Container    3792] starting compute() on background thread (current concurrency 2 of max 2) ..
2016-07-22T09:37:29+0200 [Container    3787] starting compute() on background thread (current concurrency 3 of max 3) ..
2016-07-22T09:37:29+0200 [Container    3787] compute() ended from background thread (7 invocations, current concurrency 2 of max 3)
2016-07-22T09:37:29+0200 [Container    3787] compute() ended from background thread (7 invocations, current concurrency 1 of max 3)
2016-07-22T09:37:29+0200 [Container    3787] starting compute() on background thread (current concurrency 2 of max 3) ..
2016-07-22T09:37:29+0200 [Container    3787] starting compute() on background thread (current concurrency 3 of max 3) ..
2016-07-22T09:37:31+0200 [Container    3792] compute() ended from background thread (6 invocations, current concurrency 1 of max 2)
2016-07-22T09:37:31+0200 [Container    3792] compute() ended from background thread (6 invocations, current concurrency 0 of max 2)
2016-07-22T09:37:31+0200 [Container    3787] compute() ended from background thread (9 invocations, current concurrency 2 of max 3)
2016-07-22T09:37:31+0200 [Container    3792] starting compute() on background thread (current concurrency 1 of max 2) ..
2016-07-22T09:37:31+0200 [Container    3792] starting compute() on background thread (current concurrency 2 of max 2) ..
2016-07-22T09:37:31+0200 [Container    3787] starting compute() on background thread (current concurrency 3 of max 3) ..
2016-07-22T09:37:31+0200 [Container    3787] compute() ended from background thread (10 invocations, current concurrency 2 of max 3)
2016-07-22T09:37:31+0200 [Container    3787] compute() ended from background thread (10 invocations, current concurrency 1 of max 3)
2016-07-22T09:37:31+0200 [Container    3787] starting compute() on background thread (current concurrency 2 of max 3) ..
2016-07-22T09:37:31+0200 [Container    3787] starting compute() on background thread (current concurrency 3 of max 3) ..
2016-07-22T09:37:33+0200 [Container    3792] compute() ended from background thread (8 invocations, current concurrency 1 of max 2)
2016-07-22T09:37:33+0200 [Container    3792] compute() ended from background thread (8 invocations, current concurrency 0 of max 2)
2016-07-22T09:37:33+0200 [Container    3787] compute() ended from background thread (12 invocations, current concurrency 2 of max 3)
2016-07-22T09:37:33+0200 [Container    3787] compute() ended from background thread (12 invocations, current concurrency 1 of max 3)
2016-07-22T09:37:33+0200 [Container    3787] compute() ended from background thread (12 invocations, current concurrency 0 of max 3)
```

Here is log output for the second terminal:

```console
(cpy2711_11) oberstet@thinkpad-t430s:~/scm/crossbario/crossbarexamples/concurrency-control/queued$ python client.py
2016-07-22T09:37:24+0200 session joined: SessionDetails(realm=<realm1>, session=3524239214293360, authid=<FX5M-NJHK-X5YF-HRRH-ASJH-ASKX>, authrole=<anonymous>, authmethod=anonymous, authprovider=static, authextra=None)
2016-07-22T09:37:24+0200 issueing call 0 ..
2016-07-22T09:37:24+0200 issueing call 1 ..
2016-07-22T09:37:24+0200 issueing call 2 ..
2016-07-22T09:37:24+0200 issueing call 3 ..
2016-07-22T09:37:24+0200 issueing call 4 ..
2016-07-22T09:37:24+0200 issueing call 5 ..
2016-07-22T09:37:24+0200 issueing call 6 ..
2016-07-22T09:37:24+0200 issueing call 7 ..
2016-07-22T09:37:24+0200 issueing call 8 ..
2016-07-22T09:37:24+0200 issueing call 9 ..
2016-07-22T09:37:24+0200 issueing call 10 ..
2016-07-22T09:37:24+0200 issueing call 11 ..
2016-07-22T09:37:24+0200 issueing call 12 ..
2016-07-22T09:37:24+0200 issueing call 13 ..
2016-07-22T09:37:24+0200 issueing call 14 ..
2016-07-22T09:37:24+0200 issueing call 15 ..
2016-07-22T09:37:24+0200 issueing call 16 ..
2016-07-22T09:37:24+0200 issueing call 17 ..
2016-07-22T09:37:24+0200 issueing call 18 ..
2016-07-22T09:37:24+0200 issueing call 19 ..
2016-07-22T09:37:33+0200 total run-time (wallclock): 8.04397702217
2016-07-22T09:37:33+0200 {u'call_no': 0L, u'thread': 139992138008320L, u'ended': u'2016-07-22T07:37:26.994Z', u'started': u'2016-07-22T07:37:24.992Z', u'process': 3787L, u'result': None}
2016-07-22T09:37:33+0200 {u'call_no': 1L, u'thread': 140377871247104L, u'ended': u'2016-07-22T07:37:26.995Z', u'started': u'2016-07-22T07:37:24.992Z', u'process': 3792L, u'result': None}
2016-07-22T09:37:33+0200 {u'call_no': 2L, u'thread': 139992129615616L, u'ended': u'2016-07-22T07:37:26.994Z', u'started': u'2016-07-22T07:37:24.994Z', u'process': 3787L, u'result': None}
2016-07-22T09:37:33+0200 {u'call_no': 3L, u'thread': 140377862854400L, u'ended': u'2016-07-22T07:37:26.994Z', u'started': u'2016-07-22T07:37:24.993Z', u'process': 3792L, u'result': None}
2016-07-22T09:37:33+0200 {u'call_no': 4L, u'thread': 139992121222912L, u'ended': u'2016-07-22T07:37:26.997Z', u'started': u'2016-07-22T07:37:24.994Z', u'process': 3787L, u'result': None}
2016-07-22T09:37:33+0200 {u'call_no': 5L, u'thread': 140377862854400L, u'ended': u'2016-07-22T07:37:29.002Z', u'started': u'2016-07-22T07:37:27.000Z', u'process': 3792L, u'result': None}
2016-07-22T09:37:33+0200 {u'call_no': 6L, u'thread': 140377871247104L, u'ended': u'2016-07-22T07:37:29.001Z', u'started': u'2016-07-22T07:37:26.998Z', u'process': 3792L, u'result': None}
2016-07-22T09:37:33+0200 {u'call_no': 7L, u'thread': 139992121222912L, u'ended': u'2016-07-22T07:37:29.003Z', u'started': u'2016-07-22T07:37:27.001Z', u'process': 3787L, u'result': None}
2016-07-22T09:37:33+0200 {u'call_no': 8L, u'thread': 139992129615616L, u'ended': u'2016-07-22T07:37:29.007Z', u'started': u'2016-07-22T07:37:27.004Z', u'process': 3787L, u'result': None}
2016-07-22T09:37:33+0200 {u'call_no': 9L, u'thread': 139992138008320L, u'ended': u'2016-07-22T07:37:29.007Z', u'started': u'2016-07-22T07:37:27.004Z', u'process': 3787L, u'result': None}
2016-07-22T09:37:33+0200 {u'call_no': 10L, u'thread': 140377862854400L, u'ended': u'2016-07-22T07:37:31.008Z', u'started': u'2016-07-22T07:37:29.005Z', u'process': 3792L, u'result': None}
2016-07-22T09:37:33+0200 {u'call_no': 11L, u'thread': 140377871247104L, u'ended': u'2016-07-22T07:37:31.009Z', u'started': u'2016-07-22T07:37:29.007Z', u'process': 3792L, u'result': None}
2016-07-22T09:37:33+0200 {u'call_no': 12L, u'thread': 139992138008320L, u'ended': u'2016-07-22T07:37:31.010Z', u'started': u'2016-07-22T07:37:29.008Z', u'process': 3787L, u'result': None}
2016-07-22T09:37:33+0200 {u'call_no': 13L, u'thread': 139992121222912L, u'ended': u'2016-07-22T07:37:31.013Z', u'started': u'2016-07-22T07:37:29.011Z', u'process': 3787L, u'result': None}
2016-07-22T09:37:33+0200 {u'call_no': 14L, u'thread': 139992129615616L, u'ended': u'2016-07-22T07:37:31.013Z', u'started': u'2016-07-22T07:37:29.011Z', u'process': 3787L, u'result': None}
2016-07-22T09:37:33+0200 {u'call_no': 15L, u'thread': 140377862854400L, u'ended': u'2016-07-22T07:37:33.015Z', u'started': u'2016-07-22T07:37:31.013Z', u'process': 3792L, u'result': None}
2016-07-22T09:37:33+0200 {u'call_no': 16L, u'thread': 140377871247104L, u'ended': u'2016-07-22T07:37:33.016Z', u'started': u'2016-07-22T07:37:31.013Z', u'process': 3792L, u'result': None}
2016-07-22T09:37:33+0200 {u'call_no': 17L, u'thread': 139992129615616L, u'ended': u'2016-07-22T07:37:33.017Z', u'started': u'2016-07-22T07:37:31.014Z', u'process': 3787L, u'result': None}
2016-07-22T09:37:33+0200 {u'call_no': 18L, u'thread': 139992138008320L, u'ended': u'2016-07-22T07:37:33.018Z', u'started': u'2016-07-22T07:37:31.016Z', u'process': 3787L, u'result': None}
2016-07-22T09:37:33+0200 {u'call_no': 19L, u'thread': 139992121222912L, u'ended': u'2016-07-22T07:37:33.020Z', u'started': u'2016-07-22T07:37:31.016Z', u'process': 3787L, u'result': None}
2016-07-22T09:37:33+0200 session left: CloseDetails(reason=<wamp.close.normal>, message='None')
2016-07-22T09:37:33+0200 transport disconnected
2016-07-22T09:37:33+0200 Scheduling retry 1 to connect <twisted.internet.endpoints.TCP4ClientEndpoint object at 0x7f6da5d80ed0> in 1.956610189 seconds.
2016-07-22T09:37:33+0200 Main loop terminated.
(cpy2711_11) oberstet@thinkpad-t430s:~/scm/crossbario/crossbarexamples/concurrency-control/queued$
```

