# Crossbar.io HTTP Webhook

Crossbar includes a HTTP Webhook service that is able to receive HTTP/POST requests and publish the content of them on a WAMP topic.

Webhooks are unsigned "fire and forget" notifications used by some REST services as a push notification when certain things occur.
An example is GitHub, which sends webhooks to notify services such as Travis CI that pushes have happened.

To configure the service, set up a Web transport with a path service of type `webhook` - e.g. see [.crossbar/config.json](.crossbar/config.json).
For full documentation, please see [here](http://crossbar.io/docs/HTTP-Bridge-Services/).

## Example

All HTML5 example code is in [web/index.html](web/index.html).
Python example code for making a webhook via HTTP/POSTs using the HTTP bridge built into Crossbar.io can be found here:

 * [webhook.py](webhook.py)

To publish using [curl](http://curl.haxx.se/):

```shell
curl -H "Content-Type: text/plain" \
    -d 'fresh webhooks!' \
    http://127.0.0.1:8080/webhook
```
