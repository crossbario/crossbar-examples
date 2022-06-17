# Payload Validation

**Contents**

1. [Type Catalogs](#type-catalogs)
2. [Type Inventories](#type-inventories)
   - [Local Type Catalogs](#local-type-catalogs)
   - [Network Type Catalogs](#network-type-catalogs)
3. [Realm Configuration](#realm-configuration)
   - [Static Configuration](#static-configuration)
   - [Dynamic Configuration](#dynamic-configuration)
4. [Testing](#testing)
   - [Build Catalog](#build-catalog)
   - [Start Crossbar.io](#start-crossbar)
   - [Run Test Client](#run-test-client)
   - [Open Test Pages](#open-test-pages)
---------

## Type Catalogs

*Payload Validation* is a proposed *WAMP Advanced Profile* feature for WAMP routers that allows to *define and share definitions of WAMP interfaces* written in [FlatBuffers IDL](https://google.github.io/flatbuffers/md__schemas.html).

Collections of types defined in FlatBuffers IDL are bundled in *Type Catalogs* which are just ZIP files with

* one [catalog.yaml](catalog.yaml) file with catalog metadata
* one or more `*.bfbs` compiled FlatBuffer IDL schemas

and optionally

* schema source files
* image and documentation files

The type catalog `example.zip` in this example has the following contents:

```sh
$ unzip -l ./catalogs/example/build/example.zip
Archive:  build/example.zip
  Length      Date    Time    Name
---------  ---------- -----   ----
        0  1980-00-00 00:00   schema/
    23240  1980-00-00 00:00   schema/example.bfbs
     6520  1980-00-00 00:00   schema/wamp.bfbs
     1564  1980-00-00 00:00   README.md
        0  1980-00-00 00:00   img/
    13895  1980-00-00 00:00   img/logo.png
     1070  1980-00-00 00:00   LICENSE.txt
     1212  1980-00-00 00:00   catalog.yaml
---------                     -------
    47501                     8 files
```

Above [FlatBuffers binary schema](schema/example.bfbs) is compiled

```
flatc -o ./schema --binary --schema --bfbs-comments --bfbs-builtins ./src
```

from [FlatBuffers IDL source](src/example.fbs):

```flatbuffers
rpc_service IExample1 (
    type: "interface", uuid: "bf469db0-efea-425b-8de4-24b5770e6241"
) {
    my_procedure1 (TestRequest1): TestResponse1 (
        type: "procedure", wampuri: "com.example.my_procedure1"
    );

    on_something1 (TestEvent1): Void (
        type: "topic", wampuri: "com.example.on_something1"
    );
}
```

Given this schema, and with payload validation enabled, Crossbar.io will validate:

* **calls** to `com.example.my_procedure1` must have `args/kwargs` values that match the `TestRequest1` validation type
* **call results** returned from that procedure must have `args/kwargs` values that match the `TestResponse1` validation type
* **events** published to `com.example.on_something1` must have `args/kwargs` values that match the `TestEvent1` validation type

The validation types used are also defined in the schema

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

------

## Type Inventories

Type catalogs are used at run-time in Crossbar.io in realms via *Type Inventories* by configuring an `inventory` in the respective `realm` in the Crossbar.io node configuration of the application realm:

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
                        ]
                    }
                }
            ]
        }
    ]
}
```

The only currently supported inventory type is `"wamp.eth"`, and such type inventories must have a list of catalogs. There are two supported catalog types:

1. **Local Type Catalogs**
2. **Network Type Catalogs**


### Local Type Catalogs

*Local Type Catalogs* are read from local ZIP archive files and configured by including an `archive` attribute with the file path to the catalog archive:

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
                    }
                }
            ]
        }
    ]
}
```

> As with most paths in node configuration items, the path is relative to the node directory (usually `.crossbar/`).

### Network Type Catalogs

*Network Type Catalogs* are public, shared catalogs stored in Ethereum and IPFS with optional names from ENS, and are configured by including an `address` attribute with the on-chain address of the catalog entity:

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
                    }
                }
            ]
        }
    ]
}
```

## Realm Configuration

### Static Configuration

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

* `extra`: meta arguments parsed from URI, forwarded as `Call.Details.extra|dict` or `Event.Details.extra|dict` (t.b.d.)

### Dynamic Configuration

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

### Build Catalog

For this step, you need the FlatBuffers compiler [flatc](http://google.github.io/flatbuffers/flatbuffers_guide_building.html)

```
sudo apt update
sudo apt install -y flatbuffers-compiler

OR

sudo snap install flatbuffers
```

and the archive cleaner [stripzip](https://github.com/KittyHawkCorp/stripzip)

```
make setup_stripzip
```

To build the included example catalog, and compile the FlatBuffers IDL source files to binary schemas and bundle everything into a ZIP archive:

```
cd catalogs/example
make distclean build
```

This will create `./build/example.zip`:

```
  Length      Date    Time    Name
---------  ---------- -----   ----
        0  1980-00-00 00:00   schema/
    14992  1980-00-00 00:00   schema/example2.bfbs
    16208  1980-00-00 00:00   schema/example4.bfbs
    13360  1980-00-00 00:00   schema/example3.bfbs
     8932  1980-00-00 00:00   schema/example1.bfbs
     6520  1980-00-00 00:00   schema/wamp.bfbs
     1564  1980-00-00 00:00   README.md
        0  1980-00-00 00:00   img/
    13895  1980-00-00 00:00   img/logo.png
     1070  1980-00-00 00:00   LICENSE.txt
     1288  1980-00-00 00:00   catalog.yaml
---------                     -------
    77829                     11 files
```

> IMPORTANT: The build makes sure to create the ZIP archive in a repeatable way, with files staying the same and archive metadata removed. This is crucial (!). The hash of the ZIP archive must change only when one of the contained file's *contents* changes.

### Start Crossbar

To start Crossbar.io with the [static configuration](.crossbar/config-static.json) type for payload validation:

```
make crossbar_static
```

To start Crossbar.io with the [dynamic configuration](.crossbar/config-dynamic.json) type for payload validation:

```
make crossbar_dynamic
```

### Run Test Client

To run the included test client, executing a couple test cases that work against the [backend](backend.py) included:

```
make client
```

### Open Test Pages

* [Node Info Page](http://localhost:8080/info)
* [WAMP-WebSocket Endpoint](http://localhost:8080/ws)
* [AutobahnJS](http://localhost:8080/shared/autobahn/autobahn.min.js)
* [WAMP API Catalog 1](http://localhost:8080/catalog1)
* [WAMP API Catalog 2](http://localhost:8080/catalog2)
