# Scaling Web Services

This examples demonstrates benchmarking the multi-core ready Web service built into Crossbar.io which includes services such as static file serving, WebSocket endpoints, CGI and WSGI endpoints and so on.

> Web services are powered by Twisted Web under the hood. WebSocket, WAMP and scaling on multi-core is provided by Crossbar.io.

## Requirements

The testee machine needs to have Crossbar.io installed. The load machine needs to have [wrk](https://github.com/wg/wrk) (and [weighttp](https://github.com/lighttpd/weighttp)) installed.

## Test Setup

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
