A very basic WAMP application which shows both PubSub and RPC.

Provided in three backend flavors:

* Node.js backend
* Python backend
* backend running in the browser

which all come with a browser frontend.

Additionally, there's a Python backend with a Kivy frontend in addition to the browser frontend (but you could run this with any backend, really).

Go to the respective directory and do

```sh
crossbar start
```

and open

```
http://localhost:8080
```

to see a browser fronend.

(For the Kivy version, see the README.md in the directory about additional dependencies and how to launch the frontend.)

There is also a [live version of this demo](https://demo.crossbar.io/demo/vote/web/index.html) with an annotated side-by-side display of the JavaScript code.

## Voting via curl

```
curl -H "Content-Type: application/json" \
    -d '{"procedure": "io.crossbar.demo.vote.vote", "args": ["Banana"]}' \
    https://demo.crossbar.io/call
```
