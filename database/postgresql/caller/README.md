# Crossbar.io HTTP Caller

Crossbar includes a HTTP Caller service that is able to perform WAMP calls from HTTP POST requests.

To configure the service, set up a Web transport with a path service of type `caller` - e.g. see [.crossbar/config.json](.crossbar/config.json). For full documentation, please see [here](http://crossbar.io/docs/HTTP-Bridge-Services/).

## Example

To call using [curl](http://curl.haxx.se/) (unsigned call):

```shell
curl -H "Content-Type: application/json" \
	-d '{"procedure": "com.example.add2", "args": [1, 2]}' \
	http://127.0.0.1:8080/call
```

or

```shell
curl -H "Content-Type: application/json" \
    -d '{"procedure": "com.example.add_complex", "args": [1, 2, 3, 4]}' \
    http://127.0.0.1:8080/call
```

or

```shell
curl -H "Content-Type: application/json" \
    -d '{"procedure": "com.example.split_name", "args": ["Homer Simpson"]}' \
    http://127.0.0.1:8080/call
```

or

```shell
curl -H "Content-Type: application/json" \
    -d '{"procedure": "com.example.sqrt", "args": [0]}' \
    http://127.0.0.1:8080/call
```

or

```shell
curl -H "Content-Type: application/json" \
    -d '{"procedure": "com.example.sqrt", "args": [-1]}' \
    http://127.0.0.1:8080/call
```

or

```shell
curl -H "Content-Type: application/json" \
    -d '{"procedure": "com.example.checkname", "args": ["foo"]}' \
    http://127.0.0.1:8080/call
```

or

```shell
curl -H "Content-Type: application/json" \
    -d '{"procedure": "com.example.checkname", "args": ["MixedCase"]}' \
    http://127.0.0.1:8080/call
```

or

```shell
curl -H "Content-Type: application/json" \
    -d '{"procedure": "com.example.checkname", "args": ["go"]}' \
    http://127.0.0.1:8080/call
```
