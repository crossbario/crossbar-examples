# Shared Procedures

With shared procedures, a given URI is registered by multiple endpoints.

The first registering callee defines the invocation policy for that URI. The invocation policy default is `single`, which provides the default WAMP behavior of only allowing a single callee registering a procedure.

Other invocation policies are:

* `first`
* `last`
* `roundrobin`
* `random`

## How to run

Build the app using [SCons](http://scons.org/):

```shell
scons
```

Start Crossbar by doing:

```shell
crossbar start
```

Start one or multiple backend components by starting in terminals:

```shell
./component
```

Open [`http://localhost:8080/`](http://localhost:8080/) (or wherever Crossbar runs) in your browser. Use the "call procedure" button and watch how the call is handled by one of the backends you started.
