# Payload Validation

## Type Catalogs

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

With above configuration, Crossbar.io will validate the application payloads of calls (and their results or errors) using the types refered in `validate`.

## Testing

### Test Pages

* [Node Info Page](http://localhost:8080/info)
* [WAMP-WebSocket Endpoint](http://localhost:8080/ws)
* [AutobahnJS](http://localhost:8080/shared/autobahn/autobahn.min.js)
* [WAMP API Catalog 1](http://localhost:8080/catalog1)
* [WAMP API Catalog 2](http://localhost:8080/catalog2)
