A very basic WAMP application which shows both PubSub and RPC.

Provided in three flavors:

* Node.js backend
* Python backend
* backend running in the browser

and

* Python backend with a Kivy frontend in addition to the browser frontend

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