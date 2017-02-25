# Publisher and Caller Disclosure

Open a first terminal and start Crossbar.io:

```console
ubuntu@ip-172-31-2-14:~/crossbar-examples/docker/disclose$ make crossbar
sudo docker run \
    -v /home/ubuntu/crossbar-examples/docker/disclose/crossbar:/node \
    -p 8080:8080 \
    --name crossbar \
    --rm -it crossbario/crossbar
2017-02-25T21:26:11+0000 [Controller      1]      __  __  __  __  __  __      __     __
2017-02-25T21:26:11+0000 [Controller      1]     /  `|__)/  \/__`/__`|__) /\ |__)  |/  \
2017-02-25T21:26:11+0000 [Controller      1]     \__,|  \\__/.__/.__/|__)/~~\|  \. |\__/
2017-02-25T21:26:11+0000 [Controller      1]
2017-02-25T21:26:11+0000 [Controller      1] Version:     Crossbar.io COMMUNITY 17.2.1
2017-02-25T21:26:11+0000 [Controller      1] Public Key:  b2ae03581bfa648039df59041a2273275c4623d39330a848454acf98076bcb89
2017-02-25T21:26:11+0000 [Controller      1]
2017-02-25T21:26:11+0000 [Controller      1] Node created with personality "community" [crossbar.controller.node.Node]
2017-02-25T21:26:11+0000 [Controller      1] Running from node directory "/node/.crossbar"
2017-02-25T21:26:11+0000 [Controller      1] Node configuration loaded from "/node/.crossbar/config.json"
2017-02-25T21:26:11+0000 [Controller      1] Controller process starting (CPython-EPollReactor) ..
2017-02-25T21:26:11+0000 [Controller      1] No extra node router roles
2017-02-25T21:26:11+0000 [Controller      1] Router service session attached [crossbar.router.service.RouterServiceSession]
2017-02-25T21:26:11+0000 [Controller      1] Joined realm 'crossbar' on node management router
2017-02-25T21:26:11+0000 [Controller      1] Registering management API procedure "crossbar.get_info"
2017-02-25T21:26:11+0000 [Controller      1] Registering management API procedure "crossbar.shutdown"
2017-02-25T21:26:11+0000 [Controller      1] Registering management API procedure "crossbar.get_workers"
2017-02-25T21:26:11+0000 [Controller      1] Registering management API procedure "crossbar.get_worker"
2017-02-25T21:26:11+0000 [Controller      1] Registering management API procedure "crossbar.get_worker_log"
2017-02-25T21:26:11+0000 [Controller      1] Registering management API procedure "crossbar.start_router"
2017-02-25T21:26:11+0000 [Controller      1] Registering management API procedure "crossbar.stop_router"
2017-02-25T21:26:11+0000 [Controller      1] Registering management API procedure "crossbar.start_container"
2017-02-25T21:26:11+0000 [Controller      1] Registering management API procedure "crossbar.stop_container"
2017-02-25T21:26:11+0000 [Controller      1] Registering management API procedure "crossbar.start_guest"
2017-02-25T21:26:11+0000 [Controller      1] Registering management API procedure "crossbar.stop_guest"
2017-02-25T21:26:11+0000 [Controller      1] Registering management API procedure "crossbar.start_websocket_testee"
2017-02-25T21:26:11+0000 [Controller      1] Registering management API procedure "crossbar.stop_websocket_testee"
2017-02-25T21:26:11+0000 [Controller      1] Node controller attached [crossbar.controller.process.NodeControllerSession]
2017-02-25T21:26:11+0000 [Controller      1] Using default node shutdown triggers ['shutdown_on_worker_exit']
2017-02-25T21:26:11+0000 [Controller      1] Configuring node from local configuration ...
2017-02-25T21:26:11+0000 [Controller      1] Starting 1 workers ...
2017-02-25T21:26:11+0000 [Controller      1] Starting Router with ID 'worker-001'...
2017-02-25T21:26:12+0000 [Router         13] Worker process starting (CPython-EPollReactor) ..
2017-02-25T21:26:12+0000 [Router         13] RouterWorkerSession: SessionDetails(realm=<crossbar>, session=7983007876077531, authid=<crossbar.process.13>, authrole=<crossbar.worker.worker-001>, authmethod=trusted, authprovider=programcode, authextra=None, resumed=None, resumable=None, resume_token=None)
2017-02-25T21:26:12+0000 [Controller      1] Router with ID 'worker-001' and PID 13 started
2017-02-25T21:26:12+0000 [Router         13] Realm 'realm1' started
2017-02-25T21:26:12+0000 [Controller      1] Router 'worker-001': realm 'realm-001' (named 'realm1') started
2017-02-25T21:26:12+0000 [Router         13] role role-001 on realm realm-001 started
2017-02-25T21:26:12+0000 [Controller      1] Router 'worker-001': role 'role-001' (named 'anonymous') started on realm 'realm-001'
2017-02-25T21:26:12+0000 [Router         13] started component: backend.Backend id=356862141412117
2017-02-25T21:26:12+0000 [Router         13] connected!
2017-02-25T21:26:12+0000 [Controller      1] Router 'worker-001': component 'component-001' started
2017-02-25T21:26:12+0000 [Router         13] Site starting on 8080
2017-02-25T21:26:12+0000 [Controller      1] Router 'worker-001': transport 'transport-001' started
2017-02-25T21:26:12+0000 [Controller      1] Node configuration applied successfully!
...
```

Now open a second terminal and start the Python backend component:

```console
ubuntu@ip-172-31-2-14:~/crossbar-examples/docker/disclose$ make client
sudo docker run \
    -v /home/ubuntu/crossbar-examples/docker/disclose/client:/root --link crossbar \
    --rm -it crossbario/autobahn-python:cpy3-alpine \
    python /root/client.py --url ws://crossbar:8080/ws --realm realm1
2017-02-25T21:13:20+0000 Client connected
2017-02-25T21:13:20+0000 Client session joined SessionDetails(realm=<realm1>, session=3592291800182540, authid=<CYQT-UHMG-EENT-EQAS-QXQM-375S>, authrole=<public>, authmethod=anonymous, authprovider=static, authextra=None, resumed=None, resumable=None, resume_token=None)
2017-02-25T21:13:20+0000 subscribed to topic 'onhello'
2017-02-25T21:13:20+0000 procedure add2() registered
2017-02-25T21:13:20+0000 published to 'oncounter' with counter 0
2017-02-25T21:13:22+0000 published to 'oncounter' with counter 1
2017-02-25T21:13:23+0000 published to 'oncounter' with counter 2
2017-02-25T21:13:24+0000 published to 'oncounter' with counter 3
2017-02-25T21:13:25+0000 published to 'oncounter' with counter 4
2017-02-25T21:13:26+0000 published to 'oncounter' with counter 5
^C2017-02-25T21:13:26+0000 Received SIGINT, shutting down.
2017-02-25T21:13:26+0000 Router session closed (CloseDetails(reason=<wamp.close.normal>, message='None'))
2017-02-25T21:13:26+0000 Router connection closed
2017-02-25T21:13:26+0000 Main loop terminated.
ubuntu@ip-172-31-2-14:~/crossbar-examples/docker/disclose$
```
