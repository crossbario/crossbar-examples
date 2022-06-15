# Payload Validation

## Type Catalogs

*Payload Validation* is a proposed *WAMP Avanced Profile* feature for WAMP routers allows to *define and share definitions of WAMP interfaces* written in [FlatBuffers IDL](https://google.github.io/flatbuffers/md__schemas.html).

Collections of types defined in FlatBuffers IDL can be bundled in *Type Catalogs* which are just ZIP files with

* a main `catalog.yaml` file with catalog metadata
* one or more `*.bfbs` compiled FlatBuffer IDL schemas

and optionally

* schema source files
* image and documentation files

The example here includes an [example schema](src/example.fbs) with the following interface definition:

```flatbuffers
/// Interface definition of Example 1 services.
rpc_service IExample1(type: "interface", uuid: "bf469db0-efea-425b-8de4-24b5770e6241")
{
    /// Procedure declaration for WAMP RPC.
    my_procedure1 (TestRequest1): TestResponse1 (type: "procedure", wampuri: "com.example.my_procedure1");

    /// Topic declaration for WAMP PubSub.
    on_something1 (TestEvent1): Void (type: "topic", wampuri: "com.example.on_something1");
}
```

Given this schema, and with payload validation enabled, Crossbar.io will validate:

* **calls** to `com.example.my_procedure1` must have `args/kwargs` values that match the `TestRequest1` validation type
* **call** results returned from that procedure must have `args/kwargs` values that match the `TestResponse1` validation type
* **events** published to `com.example.on_something1` must have `args/kwargs` values that match the `TestEvent1` validation type

The validation types used are also contained in the schema

```flatbuffers
struct TestData1
{
    field1: float;
    field2: int64;
}

table TestRequest1 (type: "call")
{
    field1: bool;
    field2: uint32;
    field3: uint64 (timestamp);
    field4: string (kwarg);
    field5: [uint8] (kwarg);
}

table TestResponse1 (type: "call_result")
{
    field1: uint32;
    field2: string;
    field3: bool;
    field4: TestData1;
    field5: uint64 (kwarg, timestamp);
}

table TestEvent1 (type: "event") {
    field1: string;
    field2: bool;
    field3: uint32;
    field4: uint64 (kwarg);
}
```

### Local Catalog Archives

```json
{
    "workers": [
        {
            "type": "router",
            "realms": [
                {
                    "name": "realm1",
                    "inventory": {
                        "type": "wamp.eth",
                        "catalogs": [
                            {
                                "name": "catalog1",
                                "archive": "../catalogs/example-catalog.zip"
                            }
                        ]
                    },
                }
            ]
        }
    ]
}
```

### Public Network Catalogs

```json
{
    "workers": [
        {
            "type": "router",
            "realms": [
                {
                    "name": "realm1",
                    "inventory": {
                        "type": "wamp.eth",
                        "catalogs": [
                            {
                                "name": "catalog1",
                                "address": "0x2F070c2f49a59159A0346396f1139203355ACA43"
                            }
                        ]
                    },
                }
            ]
        }
    ]
}
```


## Static Configuration

```json
{
    "workers": [
        {
            "type": "router",
            "realms": [
                {
                    "name": "realm1",
                    "roles": [
                        {
                            "name": "frontend",
                            "permissions": [
                                {
                                    "uri": "com.example.get_candle_history",
                                    "match": "exact",
                                    "allow": {
                                        "call": true,
                                        "register": false,
                                        "publish": false,
                                        "subscribe": false
                                    },
                                    "disclose": {
                                        "caller": false,
                                        "publisher": false
                                    },
                                    "validate": {
                                        "call": "trading.Period",
                                        "call_result": "trading.CandleResult",
                                        "call_error": "trading.ErrorInvalidPeriod"
                                    },
                                    "cache": true
                                }
                            ]
                        }
                    ]
                }
            ]
        }
    ]
}
```

The types refered to are provided according to *application payload type*:

* `call`: WAMP call, the (only or the initial) caller request, the `CALL.Arguments|list` and `CALL.ArgumentsKw|dict` sent by the caller (to the router)
* `call_result`: WAMP call result, the (only or the initial) callee response, in case of call success, the `RESULT.Arguments|list` and `RESULT.ArgumentsKw|dict` returned by the callee (to the router and when valid) to the caller
* `call_result_progress`: WAMP call progressive result with `RESULT.progress|bool == true`, any call result updates sent by the callee subsequently and while the call is still active
* `call_error`: WAMP call error result, the callee error response payload, in case of call failure, the `ERROR.Arguments|list` and `ERROR.ArgumentsKw|dict` returned by the callee (to the router)
* `event`: WAMP event published either using normal or router-acknowledged publications, the `EVENT.Arguments|list` and `EVENT.ArgumentsKw|dict` sent by the publisher (to the router) and dispatched by the router (when valid) to subscribers

as well as more application payload types (*FUTURE*)

* `call_progress`: WAMP call, any call updates sent by the caller subsequently and while the call is still active
* `event_confirmation`: WAMP event confirmation sent by subscribers for subscribed-confirmed publications

and meta information parsed (in the authorizer)

* `meta`: meta arguments parsed from URI


## Dynamic Configuration

*Dynamic payload validation* involves a user WAMP procedure that is called by
Crossbar.io to get *validation types* for the application payloads used in
WAMP procedures or topics.

The actual validation of a WAMP call, call result or event at run-time is done
by Crossbar.io using the (cached) validation type, without calling user code again.

To configure *dynamic payload validation*, specify the URI of your WAMP procedure:

```json
{
    "workers": [
        {
            "type": "router",
            "realms": [
                {
                    "name": "realm1",
                    "roles": [
                        {
                            "name": "frontend",
                            "authorizer": "com.example.authorize"
                        }
                    ]
                }
            ]
        }
    ]
}
```

When a client authenticated under role `frontend` on realm `realm1` is
issuing e.g. a WAMP call on a specific URI, that WAMP action ("call procedure P"), Crossbar.io will call `com.example.authorize`:

```python
class ExampleAuthorizer(ApplicationSession):

    @wamp.register('com.example.authorize')
    def authorize(self, session, uri, action, options):
        if session['authrole'] == 'frontend' and action == 'call' and \
           uri == 'com.example.get_candle_history':

            authorization = {
                'allow': True,
                'disclose': False,
                'validate': {
                    'call': 'trading.Period',
                    'call_result': 'trading.CandleResult',
                    'call_error': 'trading.ErrorInvalidPeriod'
                },
                'cache': True,
            }
            return authorization

        else:
            return False
```

With above configuration, Crossbar.io will validate the application payloads of calls (and their results or errors) to `com.example.get_candle_history` using the types referred in `validate`.

## Testing

### Test Pages

* [Node Info Page](http://localhost:8080/info)
* [WAMP-WebSocket Endpoint](http://localhost:8080/ws)
* [AutobahnJS](http://localhost:8080/shared/autobahn/autobahn.min.js)
* [WAMP API Catalog 1](http://localhost:8080/catalog1)
* [WAMP API Catalog 2](http://localhost:8080/catalog2)
