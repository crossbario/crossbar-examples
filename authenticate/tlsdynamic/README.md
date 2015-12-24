# TLS Dynamic Authentication

This uses a client-side TLS certificate to verify the connection to a server.


## How it works

The node configuration starts a router worker with a TLS listening transport:

```json
{
    "type": "web",
    "endpoint": {
        "type": "tcp",
        "port": 8080,
        "tls": {
            "key": "server.key",
            "certificate": "server.crt",
            "ca_certificates": [
                "intermediate.cert.pem",
                "ca.cert.pem"
            ],
            "dhparam": "dhparam.pem"
        }
    },
    "paths": {
        "/": {
            "type": "static",
            "directory": "../web"
        },
        "ws": {
            "type": "websocket",
            "auth": {
                "tls": {
                    "type": "dynamic",
                    "authenticator": "com.example.authenticate"
                }
            }
        }
    }
}
```

Notable configuration elements:

* `endpoint.tls.key`: The server private key.
* `endpoint.tls.certificate`: The server certificate.
* `endpoint.tls.ca_certificates`: Since this attribute is present, the server requires the client to present a client certificate. Further, the list gives the CA certificates the client certificate must be issued by.
* `paths["ws"].auth`: A dictionary of WAMP authentication methods.
* `paths["ws"].auth["tls"]`: WAMP-TLS authentication configuration.

And in this case, `paths["ws"].auth["tls"].type` specifies a `dynamic` authenticator to be used: `com.example.authenticate`.

When a client connects, it's certificate is first checked against `endpoint.tls.ca_certificates`. If the client certificate was issued by one of the CAs listed there, the authentication continues.

Later, during the WAMP opening handshake, the configured dynamic authenticator `com.example.authenticate` is called.

This is a procedure implemented by the user that will get called by Crossbar.io together with detailed information about the connecting client, including it's certificate.

The authenticator component is started inside the router worker

```json
{
   "type": "class",
   "classname": "authenticator.MyAuthenticator",
   "realm": "realm1",
   "role": "authenticator"
}
```

while the backend component is started in a container worker

```json
{
    "type": "class",
    "classname": "backend.MyBackend",
    "realm": "realm1",
    "transport": {
        "type": "websocket",
        "endpoint": {
            "type": "tcp",
            "host": "127.0.0.1",
            "port": 8080,
            "tls": {
                "hostname": "localhost",
                "key": "client.key",
                "certificate": "client.crt",
                "ca_certificates": [
                    "intermediate.cert.pem",
                    "ca.cert.pem"
                ]
            }
        },
        "url": "wss://localhost:8080/ws"
    }
}
```
