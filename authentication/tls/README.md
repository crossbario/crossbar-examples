# WAMP-TLS Authentication


## TLS listening transports

WAMP transports running over TLS can make use of TLS transport-level authentication.

E.g., here is a listening transport configuration item:

```json
"endpoint": {
    "type": "tcp",
    "port": 8080,
    "tls": {
        "key": "server.key",
        "certificate": "server.crt",
        "ca_certificates": [
            "ca.cert.pem",
            "intermediate.cert.pem"
        ]
    }
}
```

The server certificate and key to use are specified (this is required for listening transports):

* `"key": "server.key"`
* `"certificate": "server.crt"`

**Additionally**, we specify a `ca_certificates` attribute. By doing so, the server (the WAMP router) will now **require** the client to present a TLS client certificate, and the certificate must be issued by one of the listed CAs. If the client didn't present a certificate, or if it was issued by a non-listed CA, the client will be denied at the TLS transport level already.


## WAMP-TLS authentication

Consider the following snippet that configures WAMP-TLS authentication on a transport

```json
"auth": {
    "tls": {
        "type": "static",
        "principals": {
            "client_0": {
                "certificate-sha1": "B6:E5:E6:F2:2A:86:DB:3C:DC:9F:51:42:58:39:9B:14:92:5D:A1:EB",
                "role": "backend"
            }
        }
    }
}
```

WAMP authentication will kick in *after* the TLS handshake completed. If the client was denied because of unmatching TLS cert, the WAMP-level authentication won't ever start.

However, if WAMP auth kicks in, above will only allow 1 specific certificate of the given fingerprint, and then map that client to WAMP authid `client_0` and role `backend`.

So this control is at a finer level (per-certificate, not only issuing CAs), and it also provide mapped WAMP `authid` and `authrole`.

The WAMP-TLS authentication mechanism is available in **static mode**, where as in above, the principals are configured statically in the Crossbar.io node configuration.

But you can take over full control by using **dynamic mode**, where you provide an authenticator procedure to be called that checks the client certificate and grants access or not.


## TLS connecting transports

Consider the following snipped that configures a WAMP **connecting transport** (e.g. for use from a container component):

```json
"endpoint": {
    "type": "tcp",
    "host": "127.0.0.1",
    "port": 8080,
    "tls": {
        "hostname": "localhost",
        "key": "client.key",
        "certificate": "client.crt",
        "ca_certificates": [
            "ca.cert.pem",
            "intermediate.cert.pem"
        ]
    }
}
```

The client certificate and key to use are specified (this is optional for connecting transports):

* `"key": "client.key"`
* `"certificate": "client.crt"`

Additionally, we specify a `ca_certificates` attributes. By doing so, the TLS server we connect to will no longer be verified against the system/platform trust store (the default when `ca_certificates` is NOT there), but we verified against the CA certificates listed.
