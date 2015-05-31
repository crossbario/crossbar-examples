This example demonstrates the [WAMP-over-Longpoll](http://crossbar.io/docs/WAMP-Long-Poll-Service/) transport service included with Crossbar.io together with AutobahnJS.

Using this transport allows to use WAMP with old browsers that lack WebSocket support (most relevant to IE<10 and old Android WebKit).


## How to run

To run, start the node

```console
crossbar start
```

and point your browser to [http://localhost:8080](http://localhost:8080).

Open the JS console to see the log output.

Then press the "open session" button.

You should see events being received and logged in the JS console.

## How it works

Have a look at these lines from the `index.html`

```javascript
         var connection = new autobahn.Connection({
            transports: [
/*
               {
                  'type': 'websocket',
                  'url': 'ws://' + document.location.host + '/ws',
               },
*/
               {
                  'type': 'longpoll',
                  'url': 'http://' + document.location.host + '/lp',
               }
            ],
            realm: 'realm1'
         });
```

AutobahnJS is able to create a WAMP connection by trying transports from a list until a working transport is found.

Here, we have commented `websocket`, so even a modern browser will connect via Longpoll. Normally, you would have the `websocket` transport also, so Longpoll is *only* used when the browser does not support WebSocket.
