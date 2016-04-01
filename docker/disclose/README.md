# Publisher and Caller Disclosure

Open a first terminal and start Crossbar.io:

```console
oberstet@thinkpad-t430s:~/scm/crossbario/crossbarexamples/docker/disclose$ make crossbar
# FIXME: the Docker image runs Crossbar.io under user "daemon" - make sure it can write
chmod 777 ./crossbar/.crossbar
sudo docker run -v /home/oberstet/scm/crossbario/crossbarexamples/docker/disclose/crossbar:/var/crossbar \
        -p 8080:8080 \
        -it crossbario/crossbar
2016-03-27T21:52:46+0000 [Controller      1] Automatically choosing optimal Twisted reactor
2016-03-27T21:52:46+0000 [Controller      1] Running on Linux and optimal reactor (epoll) was installed.
2016-03-27T21:52:46+0000 [Controller      1]      __  __  __  __  __  __      __     __
2016-03-27T21:52:46+0000 [Controller      1]     /  `|__)/  \/__`/__`|__) /\ |__)  |/  \
2016-03-27T21:52:46+0000 [Controller      1]     \__,|  \\__/.__/.__/|__)/~~\|  \. |\__/
2016-03-27T21:52:46+0000 [Controller      1]
2016-03-27T21:52:46+0000 [Controller      1]     Crossbar.io Version: 0.13.0
2016-03-27T21:52:46+0000 [Controller      1]     Node Public Key: 077ce3e1407cf2d994ccd3138f80e4ac7b4542dda19daea1fc5d47e6dea95399
2016-03-27T21:52:46+0000 [Controller      1]
2016-03-27T21:52:46+0000 [Controller      1] Running from node directory '/var/crossbar/.crossbar'
2016-03-27T21:52:46+0000 [Controller      1] Controller process starting (PyPy-EPollReactor) ..
2016-03-27T21:52:46+0000 [Controller      1] Node configuration loaded from 'config.json'
2016-03-27T21:52:46+0000 [Controller      1] Node ID '4d059d141e7c' set from hostname
2016-03-27T21:52:46+0000 [Controller      1] Using default node shutdown triggers [u'shutdown_on_worker_exit']
2016-03-27T21:52:46+0000 [Controller      1] Joined realm 'crossbar' on node management router
2016-03-27T21:52:47+0000 [Controller      1] Starting Router with ID 'worker1'...
2016-03-27T21:52:47+0000 [Router         12] Worker process starting (PyPy-EPollReactor) ..
2016-03-27T21:52:48+0000 [Controller      1] Router with ID 'worker1' and PID 12 started
2016-03-27T21:52:48+0000 [Router         12] Realm 'realm1' started
2016-03-27T21:52:48+0000 [Controller      1] Router 'worker1': realm 'realm1' (named 'realm1') started
2016-03-27T21:52:48+0000 [Controller      1] Router 'worker1': role 'role1' (named 'anonymous') started on realm 'realm1'
2016-03-27T21:52:48+0000 [Router         12] Site starting on 8080
2016-03-27T21:52:48+0000 [Controller      1] Router 'worker1': transport 'transport1' started
...
```

Now open a second terminal and start the Python backend component:

```console
oberstet@thinkpad-t430s:~/scm/crossbario/crossbarexamples/docker/disclose$ make client
sudo docker run -v /home/oberstet/scm/crossbario/crossbarexamples/docker/disclose/client:/root \
        -it crossbario/autobahn-python:cpy3-alpine \
        python /root/client.py --url ws://192.168.55.135:8080/ws --realm realm1
2016-03-27T21:53:27+0000 Client connected
2016-03-27T21:53:27+0000 Client session joined SessionDetails(realm=<realm1>, session=6469278897990119, authid=<W3AT-JVY9-LJCF-9NYJ-REAM-ULHW>, authrole=<anonymous>, authmethod=anonymous, authprovider=static, authextra=None)
2016-03-27T21:53:27+0000 subscribed to topic 'onhello'
2016-03-27T21:53:27+0000 procedure add2() registered
2016-03-27T21:53:27+0000 published to 'oncounter' with counter 0
2016-03-27T21:53:28+0000 published to 'oncounter' with counter 1
2016-03-27T21:53:29+0000 published to 'oncounter' with counter 2
...
```

Now point your browser to [http://localhost:8080](http://localhost:8080) and press F12 to watch the JavaScript debugging console. You should see messages being logged.

In the terminal running the Python backend component, you should see:

```console
...
016-03-27T21:54:50+0000 mul2() called with result: 249
2016-03-27T21:54:50+0000 event for 'onhello' received: Hello from JavaScript (browser) EventDetails(publication=3525894990683457, publisher=3861958618172234, publisher_authid=7TXN-HTPJ-STSQ-J5HE-VS3L-P9VC, publisher_authrole=anonymous, topic=<com.example.onhello>, enc_algo=None)
2016-03-27T21:54:50+0000 add2() called with 192 and 18 - CallDetails(progress=None, caller=3861958618172234, caller_authid=7TXN-HTPJ-STSQ-J5HE-VS3L-P9VC, caller_authrole=anonymous, procedure=<com.example.add2>, enc_algo=None)
2016-03-27T21:54:51+0000 published to 'oncounter' with counter 83
2016-03-27T21:54:51+0000 mul2() called with result: 252
2016-03-27T21:54:51+0000 event for 'onhello' received: Hello from JavaScript (browser) EventDetails(publication=288804218554371, publisher=3861958618172234, publisher_authid=7TXN-HTPJ-STSQ-J5HE-VS3L-P9VC, publisher_authrole=anonymous, topic=<com.example.onhello>, enc_algo=None)
2016-03-27T21:54:51+0000 add2() called with 195 and 18 - CallDetails(progress=None, caller=3861958618172234, caller_authid=7TXN-HTPJ-STSQ-J5HE-VS3L-P9VC, caller_authrole=anonymous, procedure=<com.example.add2>, enc_algo=None)
2016-03-27T21:54:52+0000 event for 'onhello' received: Hello from JavaScript (browser) EventDetails(publication=4026698264089087, publisher=3861958618172234, publisher_authid=7TXN-HTPJ-STSQ-J5HE-VS3L-P9VC, publisher_authrole=anonymous, topic=<com.example.onhello>, enc_algo=None)
2016-03-27T21:54:52+0000 add2() called with 198 and 18 - CallDetails(progress=None, caller=3861958618172234, caller_authid=7TXN-HTPJ-STSQ-J5HE-VS3L-P9VC, caller_authrole=anonymous, procedure=<com.example.add2>, enc_algo=None)
2016-03-27T21:54:52+0000 published to 'oncounter' with counter 84
2016-03-27T21:54:52+0000 mul2() called with result: 255
2016-03-27T21:54:53+0000 event for 'onhello' received: Hello from JavaScript (browser) EventDetails(publication=7896362031254924, publisher=3861958618172234, publisher_authid=7TXN-HTPJ-STSQ-J5HE-VS3L-P9VC, publisher_authrole=anonymous, topic=<com.example.onhello>, enc_algo=None)
2016-03-27T21:54:53+0000 add2() called with 201 and 18 - CallDetails(progress=None, caller=3861958618172234, caller_authid=7TXN-HTPJ-STSQ-J5HE-VS3L-P9VC, caller_authrole=anonymous, procedure=<com.example.add2>, enc_algo=None)
2016-03-27T21:54:53+0000 published to 'oncounter' with counter 85
2016-03-27T21:54:53+0000 mul2() called with result: 258
...
```
