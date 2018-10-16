# Crossbar.io HTTP Subscriber

Crossbar includes a HTTP Subscriber which forwards WAMP PubSub messages to a HTTP server.
The message is serialised to JSON and (by default) HTTP POSTed to a URL.

To configure the service, set up a component with the classname `crossbar.adapter.rest.MessageForwarder` - e.g. see [.crossbar/config.json](.crossbar/config.json). For full documentation, please see [here](https://crossbar.io/docs/HTTP-Bridge/).

## Example

To publish a message using [curl](http://curl.haxx.se/) (unsigned call):

```shell
curl -H "Content-Type: application/json" \
	-d '{"topic": "com.myapp.topic1", "args": ["Hello, world"]}' \
	http://127.0.0.1:8080/publish
```

This example configuration will then forward the message to `httpbin.org/post` (which echos back what was sent to it) and print out the response in the controller's debug log.
