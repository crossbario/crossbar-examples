# Crossbar.io HTTP Callee

Crossbar includes a HTTP Callee module that is able to perform HTTP requests from WAMP calls.

To configure the service, set up a component with the classname `crossbar.adapter.rest.RESTCallee` - e.g. see [.crossbar/config.json](.crossbar/config.json). For full documentation, please see [here](http://crossbar.io/docs/HTTP-Bridge-Services/).

## Example

To test using [curl](http://curl.haxx.se/) (unsigned call):

```shell
curl -H "Content-Type: application/json" \
	-d '{"procedure": "com.myapp.rest", "kwargs": {"url": "get", "method": "GET"}}' \
	http://127.0.0.1:8080/call
```

This will "call" `httpbin.org/get` (which echos requests) and will respond with the request's result.
