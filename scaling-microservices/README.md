# Transparent scaling of microservices

Crossbar.io supports a number of features that when combined provide **transparent scale-out of microservices**:

1. shared registrations
2. concurrency control
3. call queuing

> You will need Crossbar.io and AutobahnPython >= 0.15.0 for the latter 2 features.

For a complete example, please see [here](queued/README.md).

## Introduction

### Shared registrations

Normally, a procedure can only be registered by one WAMP client (= microservice instance). Another client that wants to register the same URI for a procedure will get a "already registered" error.

Crossbar.io however supports **shared registrations**.

With shared registrations, multiple clients or instances of a microservice can register a procedure under the *same URI*, while specifying a **invocation policy**:

* single, first, last
* round-robin
* random

For example, with round-robin

```python
yield self.register(self.compute,
                    u'com.example.compute',
                    options=RegisterOptions(invoke=u'roundrobin'))
```

Crossbar.io will forward calls incoming for the respective procedure URI to all microservice instances that have registered the URI in a round-robin fashion.

This allows basic scale-out of microservices.

### Concurrency control

A problem with the naive approach above is: when there are more calls incoming than the backend microservices (the callees) can handle, Crossbar.io will nevertheless continue to forward calls to the (already overloaded) clients implementing the procedure.

What is needed is a way for a callee to specify the **maximum concurrency** at which it is able to serve calls. The maximum concurrency is the number of calls a callee can practically process in parallel (doing useful work, instead of mere piling up the incoming procedure invocations).

Autobahn and Crossbar.io support this using a option during registering a procedure, eg:

```python
yield self.register(self.compute,
                    u'com.example.compute',
                    options=RegisterOptions(concurrency=4))
```

With above, Crossbar.io will never forward more than 4 calls concurrently to the callee. When a 5th call comes in, this call will be immediately denied with "maximum concurrency reached".

This error can then act as a backpressure signal to the caller to reduce its rate of issueing calls and prevents overloading a callee.

### Call queueing

Backpressure signaling is one way of handling the problem of overloaded callee instances. Another way is **call queueing**.

With call queueing, Crossbar.io will queue up calls internally when the callees maximum concurrency have been reached, and then later forward calls when the load on callees is lowering again.

This feature needs to be enabled in the Crossbar.io configuration:

```json
"realms": [
    {
        "name": "realm1",
        "roles": [
            ...
        ],
        "store": {
            "type": "memory",
            "call-queue": [
                {
                    "uri": "com.example.compute",
                    "match": "exact",
                    "limit": 1000
                }
            ]
        }
    }
]
```

With above, Crossbar.io will queue up calls in memory up to a limit of 1000 when the callee side of `com.example.compute` becomes overloaded.
