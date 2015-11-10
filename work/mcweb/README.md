# Scaling Web Services

This examples demonstrates benchmarking the multi-core ready Web service built into Crossbar.io. The Web services that are available include static file hosting, file upload, WebSocket endpoints, CGI and WSGI endpoints and more.

> Web services are powered by [Twisted Web](http://twistedmatrix.com/documents/current/web/howto/using-twistedweb.html) under the hood. WebSocket, WAMP and scaling on multi-core is provided by Crossbar.io.

## Requirements

The testee machine needs to have Crossbar.io installed. The load machine needs to have [wrk](https://github.com/wg/wrk) and [weighttp](https://github.com/lighttpd/weighttp) installed.

## Test Setup

The tests were run on two identical machines, each with:

* Single-socket Intel Xeon E3-1240 v3 CPU, Quad-core (with 8 HT), 3.4GHz and 32GB ECC RAM
* Dual-port 10GbE Intel X540-T2 Ethernet adapter

Both machines were connected over a 10GbE switch.

The testee machine (with Crossbar.io) was running under Ubuntu 14.03 LTS, while the load machine (with wrk/weighttp) was running FreeBSD 10.2.

## Test Procedure

In a first terminal, login to the testee machine ("brummer2") and start Crossbar.io with a given number of workers:

```
make crossbar_w8
```

In a second terminal, login to the load machine ("brummer1") and set the testee's HTTP URL in the `TESTEE` environment variable:

```
export TESTEE=http://10.0.1.3:8080
```

Now start the load generator, redirecting output to a log file:

```
make test > results/result_w8_1.log
```

Repeat the last step (**without** restarting Crossbar.io) and number of times, producing multiple result files for a single test run ("result_w8_1.log", ...).

## How it works

Crossbar.io is started from a local node configuration. Here is the one used for the tests with 1 worker:

```json
{
   "workers": [
      {
         "options": {
            "cpu_affinity": [
               0
            ],
            "pythonpath": [
               ".."
            ]
         },
         "transports": [
            {
               "endpoint": {
                  "backlog": 2048,
                  "port": 8080,
                  "shared": true,
                  "type": "tcp"
               },
               "paths": {
                  "/": {
                     "directory": "..",
                     "type": "static"
                  },
                  "json": {
                     "type": "json",
                     "value": {
                        "param1": "foobar",
                        "param2": [
                           1,
                           2,
                           3
                        ],
                        "param3": {
                           "awesome": true,
                           "nifty": "yes"
                        }
                     }
                  },
                  "resource": {
                     "classname": "myresource.MyResource",
                     "type": "resource"
                  }
               },
               "type": "web"
            }
         ],
         "type": "router"
      }
   ]
}
```

The node configuration contains a `"workers"` attribute in a top-level dictionary which is a list of worker items.

Each worker item is a dictionary, with a `"type"`, possibly `"options"` and a `"transports"` list.

The transport is of `"type": "web"`, and configures 3 Web services on the paths `/`, `/json` and `/resource`.

The `/` path is configured to serve static files over HTTP from the folder `..`, relative to the node configuration.

The `/json` path is configured to serve a serialized JSON value as specified in the configuration.

The `/resource` path is configured to serve a Twisted Web resource written by us and contained in [myresource.py](myresource.py).

The configuration files for more workers replicates above, with the only adjustment being the CPU affinity set for each worker.

> Setting the CPU affinity is a performance optimization.
