# Network Monitor

This example uses crossbar.io to pass simulated network events from a
python publisher to a browser client subscriber.

## Why is this a good example?

* mixes twisted and autobahn code
* python app is stand-alone and not purely an ApplicationSession 
* javascript client is a lot prettier than the console log
* React.js is used for a more realistic _real world_ example

## Why is this a bad example

* this is the authors first Crossbar.io app
* this is the authors first React.js app

So use any code with a grain of salt. Having said that it should get you
started.

## Installation

```
# make a virtual environment and activate it
pip install crossbar setproctitle
```

## Running

```
crossbar start
```

Open browser to: localhost:9001

Hit `ctrl-c` in terminal to stop crossbar process.

## What's happening

Crossbar is a router (message broker, etc) that is also a process
starter and monitor.

When crossbar starts, it also starts netmonitor, a simple daemon that
publishes simulated network events.

Crossbar is also a simple webserver, so when you browse to
`http://localhost:8080` you get served `client/index.html`.

