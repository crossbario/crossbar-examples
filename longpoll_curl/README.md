# WAMP-over-Longpoll using curl

This example demonstrates how to access the WAMP-over-Longpoll service of Crossbar.io using **curl** only.

This example is mostly for developers of WAMP client libraries that want to support WAMP-over-Longpoll.

It is **not** for end-users - as using curl to do WAMP is a PITA;)


## How to run

Here is how to test the *Long-Poll Service* using [curl](http://curl.haxx.se/). Of course, you wouldn't be using curl in your app, but you can use it to e.g. develop a client library supporting WAMP-over-Longpoll.

To run, open 3 terminals.

In the first terminal

```console
make crossbar
```

In the second terminal

```console
make subscribe
```

In the third terminal

```console
make receive
```

### Log output

Here is the log output of the latter two terminals running curl.

First terminal (subscriber):

```console
oberstet@thinkpad-t430s:~/scm/crossbar/crossbarexamples/longpoll_curl$ make subscribe
Opening session
curl -H "Content-Type: application/json" -d '{"protocols": ["wamp.2.json"]}' http://127.0.0.1:8080/lp/open
{"protocol": "wamp.2.json", "transport": "kjmd3sBLOUnb3Fyr"}

Joining realm
curl -H "Content-Type: application/json" -d '[1, "realm1", {"roles": {"subscriber": {}, "publisher": {}}}]' http://127.0.0.1:8080/lp/kjmd3sBLOUnb3Fyr/send
curl -H "Content-Type: application/json" -d '' http://127.0.0.1:8080/lp/kjmd3sBLOUnb3Fyr/receive
[2,166310667,{"authrole":"anonymous","authmethod":"anonymous","roles":{"broker":{"features":{"publisher_identification":true,"pattern_based_subscription":true,"subscription_meta_api":true,"subscription_revocation":true,"publisher_exclusion":true,"subscriber_blackwhite_listing":true}},"dealer":{"features":{"pattern_based_registration":true,"registration_revocation":true,"shared_registration":true,"caller_identification":true,"registration_meta_api":true,"progressive_call_results":true}}},"authid":"0W-15aZtVXY2HubWhK72aNrO"}]

Subscribing to topic
curl -H "Content-Type: application/json" -d '[32, 1, {}, "com.myapp.topic1"]' http://127.0.0.1:8080/lp/kjmd3sBLOUnb3Fyr/send
curl -H "Content-Type: application/json" -d '' http://127.0.0.1:8080/lp/kjmd3sBLOUnb3Fyr/receive
[33,1,1938715971]

Waiting for event ..
curl -H "Content-Type: application/json" -d '' http://127.0.0.1:8080/lp/kjmd3sBLOUnb3Fyr/receive
[36,1938715971,459237991,{},["Hello, world!",23,666]]

oberstet@thinkpad-t430s:~/scm/crossbar/crossbarexamples/longpoll_curl$
```

Second terminal (publisher):

```console
oberstet@thinkpad-t430s:~/scm/crossbar/crossbarexamples/longpoll_curl$ make publish
Opening session
curl -H "Content-Type: application/json" -d '{"protocols": ["wamp.2.json"]}' http://127.0.0.1:8080/lp/open
{"protocol": "wamp.2.json", "transport": "kjmd3sBLOUnb3Fyr"}

Joining realm
curl -H "Content-Type: application/json" -d '[1, "realm1", {"roles": {"subscriber": {}, "publisher": {}}}]' http://127.0.0.1:8080/lp/kjmd3sBLOUnb3Fyr/send
curl -H "Content-Type: application/json" -d '' http://127.0.0.1:8080/lp/kjmd3sBLOUnb3Fyr/receive
[2,408582366,{"authrole":"anonymous","authmethod":"anonymous","roles":{"broker":{"features":{"publisher_identification":true,"pattern_based_subscription":true,"subscription_meta_api":true,"subscription_revocation":true,"publisher_exclusion":true,"subscriber_blackwhite_listing":true}},"dealer":{"features":{"pattern_based_registration":true,"registration_revocation":true,"shared_registration":true,"caller_identification":true,"registration_meta_api":true,"progressive_call_results":true}}},"authid":"lmIqXAiMI_g31MFIVTWhbCf2"}]

Publishing event to topic
curl -H "Content-Type: application/json" -d '[16, 1, {}, "com.myapp.topic1", ["Hello, world!", 23, 666]]' http://127.0.0.1:8080/lp/kjmd3sBLOUnb3Fyr/send

Closing session
curl -H "Content-Type: application/json" -d '' http://127.0.0.1:8080/lp/kjmd3sBLOUnb3Fyr/close
```

## How it works

We are using the following config for Crossbar.io:

```javascript
{
   "workers": [
      {
         "type": "router",
         "options": {
            "pythonpath": [".."]
         },
         "realms": [
            {
               "name": "realm1",
               "roles": [
                  {
                     "name": "anonymous",
                     "permissions": [
                        {
                           "uri": "*",
                           "publish": true,
                           "subscribe": true,
                           "call": true,
                           "register": true
                        }
                     ]
                  }
               ]
            }
         ],
         "transports": [
            {
               "type": "web",
               "endpoint": {
                  "type": "tcp",
                  "port": 8080
               },
               "paths": {
                  "/": {
                     "type": "static",
                     "directory": ".."
                  },
                  "ws": {
                     "type": "websocket"
                  },
                  "lp": {
                     "type": "longpoll",
                     "options": {
                        "debug": true,
                        "debug_transport_id": "kjmd3sBLOUnb3Fyr",
                        "session_timeout": 0
                     }
                  }
               }
            }
         ]
      }
   ]
}
```

Above config enables debug mode, and sets a fixed transport ID `kjmd3sBLOUnb3Fyr`. Setting a fixed transport ID is useful for development and debugging purposes.


### Subscribing

We first **open** a new transport session

```console
curl -H "Content-Type: application/json" \
    -d '{"protocols": ["wamp.2.json"]}' \
    http://127.0.0.1:8080/lp/open
```

This will return the **tranport ID** `kjmd3sBLOUnb3Fyr` which we subsequently use in our request.

We **join** a realm by sending a WAMP `HELLO` message

```console
curl -H "Content-Type: application/json" \
    -d '[1, "realm1", {"roles": {"subscriber": {}, "publisher": {}}}]' \
    http://127.0.0.1:8080/lp/kjmd3sBLOUnb3Fyr/send
```

and fetch the WAMP `WELCOME` message sent to us by the router

```console
curl -H "Content-Type: application/json" \
    -d '' \
    http://127.0.0.1:8080/lp/kjmd3sBLOUnb3Fyr/receive
```

We then **subscribe** to a topic by sending a WAMP `SUBSCRIBE` message

```console
curl -H "Content-Type: application/json" \
    -d '[32, 1, {}, "com.myapp.topic1"]' \
    http://127.0.0.1:8080/lp/kjmd3sBLOUnb3Fyr/send
```

and fetch the WAMP `SUBSCRIBED` message acknowledge from the router:

```console
curl -H "Content-Type: application/json" \
    -d '' \
    http://127.0.0.1:8080/lp/kjmd3sBLOUnb3Fyr/receive
```

Finally we long-poll to receive events (actually, we wait for any WAMP message for us to become available)

```console
curl -H "Content-Type: application/json" \
    -d '' \
    http://127.0.0.1:8080/lp/kjmd3sBLOUnb3Fyr/receive
```

The latter request will not return until there is a WAMP message available to be received (such as an event published on the topic we subscribed to).


### Publishing

The first couple of steps are identical to above. Where it differs is when we **publish** a message instead of subscribing:

```console
curl -H "Content-Type: application/json" \
    -d '[16, 1, {}, "com.myapp.topic1", ["Hello, world!", 23, 666]]' \
    http://127.0.0.1:8080/lp/kjmd3sBLOUnb3Fyr/send
```

After publishing the event, the long-poll request in the first terminal will return with the event.

Finally, to close the session

```
curl -H "Content-Type: application/json" \
    -d '' \
    http://127.0.0.1:8080/lp/kjmd3sBLOUnb3Fyr/close
```

> Note: Normally, the two sessions above would have had different transport IDs. Since we use a fixed transport ID (via the `debug_transport_id` option), *both* sessions will be closed!
