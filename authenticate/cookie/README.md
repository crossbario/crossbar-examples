To run this example

    crossbar start

Then open [`http://localhost:8080`](http://localhost:8080) in your browser. Open the JavaScript console.

The **first time** you open this page you should see a log similar to this:

```text
AutobahnJS debug enabled
(index):16 Ok, AutobahnJS loaded 0.9.7
autobahn.min.js:32 trying to create WAMP transport of type: websocket
autobahn.min.js:32 using WAMP transport type: websocket
autobahn.min.js:32 WebSocket transport send [1,"realm1",{"roles":{"caller":{"features":{"caller_identification":true,"progressive_call_results":true}},"callee":{"features":{"caller_identification":true,"pattern_based_registration":true,"shared_registration":true,"progressive_call_results":true,"registration_revocation":true}},"publisher":{"features":{"publisher_identification":true,"subscriber_blackwhite_listing":true,"publisher_exclusion":true}},"subscriber":{"features":{"publisher_identification":true,"pattern_based_subscription":true,"subscription_revocation":true}}},"authmethods":["cookie","wampcra"],"authid":"joe"}]
autobahn.min.js:32 WebSocket transport receive [4,"wampcra",{"challenge":"{\"nonce\": \"bp7d9mJ4RQlCVN7v\", \"authprovider\": \"static\", \"authid\": \"joe\", \"timestamp\": \"2015-08-24T12:12:55.812Z\", \"authrole\": \"frontend\", \"authmethod\": \"wampcra\", \"session\": 1131593967612115}"}]
(index):25 onchallenge wampcra Object {challenge: "{"nonce": "bp7d9mJ4RQlCVN7v", "authprovider": "sta…hmethod": "wampcra", "session": 1131593967612115}"}
(index):29 authenticating via 'wampcra' and challenge '{"nonce": "bp7d9mJ4RQlCVN7v", "authprovider": "static", "authid": "joe", "timestamp": "2015-08-24T12:12:55.812Z", "authrole": "frontend", "authmethod": "wampcra", "session": 1131593967612115}'
autobahn.min.js:32 WebSocket transport send [5,"Cwy62EN7loBuU/bsGtA6yptiGFuGvUXQfBPRJhS5c48=",{}]
autobahn.min.js:32 WebSocket transport receive [2,1131593967612115,{"authrole":"frontend","authmethod":"wampcra","authprovider":"static","roles":{"broker":{"features":{"publisher_identification":true,"pattern_based_subscription":true,"subscription_meta_api":true,"subscription_revocation":true,"publisher_exclusion":true,"subscriber_blackwhite_listing":true}},"dealer":{"features":{"pattern_based_registration":true,"registration_revocation":true,"shared_registration":true,"caller_identification":true,"registration_meta_api":true,"progressive_call_results":true}}},"authid":"joe"}]
(index):51 connected session with ID 1131593967612115
(index):52 authenticated using method 'wampcra' and provider 'static'
(index):53 authenticated with authid 'joe' and authrole 'frontend'
autobahn.min.js:32 WebSocket transport send [48,2332246451159040,{},"com.example.add2",[2,3]]
autobahn.min.js:32 WebSocket transport receive [50,2332246451159040,{},[5]]
(index):59 call result 5
```

What you can see from above log is that the client announced to be willing to authenticate using `authmethods == ["cookie","wampcra"]`.

Crossbar.io decided to go with `wampcra` and send an authentication `CHALLENGE`  message to the client, which the client responded to with a signature.

The client is then accepted, and Crossbar.io informs about the effective authentication that was used: `"authmethod": "wampcra"` and `"authprovider": "static"`.

The **second time** you open this page you should see a log similar to this:

```text
AutobahnJS debug enabled
(index):16 Ok, AutobahnJS loaded 0.9.7
autobahn.min.js:32 trying to create WAMP transport of type: websocket
autobahn.min.js:32 using WAMP transport type: websocket
autobahn.min.js:32 WebSocket transport send [1,"realm1",{"roles":{"caller":{"features":{"caller_identification":true,"progressive_call_results":true}},"callee":{"features":{"caller_identification":true,"pattern_based_registration":true,"shared_registration":true,"progressive_call_results":true,"registration_revocation":true}},"publisher":{"features":{"publisher_identification":true,"subscriber_blackwhite_listing":true,"publisher_exclusion":true}},"subscriber":{"features":{"publisher_identification":true,"pattern_based_subscription":true,"subscription_revocation":true}}},"authmethods":["cookie","wampcra"],"authid":"joe"}]
autobahn.min.js:32 WebSocket transport receive [2,3522335203904621,{"authrole":"frontend","authmethod":"wampcra","authprovider":"cookie","roles":{"broker":{"features":{"publisher_identification":true,"pattern_based_subscription":true,"subscription_meta_api":true,"subscription_revocation":true,"publisher_exclusion":true,"subscriber_blackwhite_listing":true}},"dealer":{"features":{"pattern_based_registration":true,"registration_revocation":true,"shared_registration":true,"caller_identification":true,"registration_meta_api":true,"progressive_call_results":true}}},"authid":"joe"}]
(index):51 connected session with ID 3522335203904621
(index):52 authenticated using method 'wampcra' and provider 'cookie'
(index):53 authenticated with authid 'joe' and authrole 'frontend'
autobahn.min.js:32 WebSocket transport send [48,1299945168568320,{},"com.example.add2",[2,3]]
autobahn.min.js:32 WebSocket transport receive [50,1299945168568320,{},[5]]
(index):59 call result 5
```

As you can see, this time Crossbar.io directly accepted the client. It also informs the client that it was using `"authmethod": "wampcra"` and `"authprovider": "cookie"`.

This is reflected in the cookie file where Crossbar.io persists the cookies:

```console
(python279_1)oberstet@thinkpad-t430s:~/scm/crossbar/crossbarexamples/authenticate/cookie$ cat .crossbar/cookies.dat
{"max_age": 604800, "authid": null, "authrole": null, "authmethod": null, "created": "2015-08-24T13:45:33.381Z", "id": "MXRQadHFItz75_-FSxk9g-xg"}
{"max_age": 604800, "authid": "joe", "authrole": "frontend", "authmethod": "wampcra", "modified": "2015-08-24T13:45:33.381Z", "id": "MXRQadHFItz75_-FSxk9g-xg"}
```

It is also reflected in the Crossbar.io log.

First time start:

```console
2015-08-24T15:45:28+0200 [Router      11874] Loaded 0 cookie records from file. Cookie store has 0 entries.
2015-08-24T15:45:28+0200 [Router      11874] File-backed cookie store active /home/oberstet/scm/crossbar/crossbarexamples/authenticate/cookie/.crossbar/cookies.dat
```

Second time start:

```console
2015-08-24T15:46:23+0200 [Router      11903] Loaded 2 cookie records from file. Cookie store has 1 entries.
2015-08-24T15:46:23+0200 [Router      11903] File-backed cookie store active /home/oberstet/scm/crossbar/crossbarexamples/authenticate/cookie/.crossbar/cookies.dat
```
