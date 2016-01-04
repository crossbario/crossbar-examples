# TLS Dynamic Authentication

This uses a client-side TLS certificate to authenticate a WAMP session using a **dynamic authenticator**.

A WAMP router worker is started that runs a TLS transport and embeds a dynamic authenticator user component.
A container worker is started with a backend component that connects via TLS and presents a TLS client certificate.
The client certificate is verified against a server-side CA cert list, and then dynamically authenticated by calling the dynamic authenticator we prodive.


## How to test

Start Crossbar.io from this directory. You should see log output like the following up to the `"MyBackend: procedure add2() registered"` log message, which indicates that the backend component has successfully authenticated and registered it's backend procedure.

```console
(python279_1)oberstet@thinkpad-t430s:~/scm/crossbario/crossbarexamples/authenticate/tlsdynamic$ make test
PYTHONPATH=../../../crossbar python -m crossbar.controller.cli start
2015-12-24T19:52:49+0100 [Controller  27108]      __  __  __  __  __  __      __     __
2015-12-24T19:52:49+0100 [Controller  27108]     /  `|__)/  \/__`/__`|__) /\ |__)  |/  \
2015-12-24T19:52:49+0100 [Controller  27108]     \__,|  \\__/.__/.__/|__)/~~\|  \. |\__/
2015-12-24T19:52:49+0100 [Controller  27108]
2015-12-24T19:52:49+0100 [Controller  27108]     Version: 0.11.2
2015-12-24T19:52:49+0100 [Controller  27108]
2015-12-24T19:52:49+0100 [Controller  27108] Running from node directory '/home/oberstet/scm/crossbario/crossbarexamples/authenticate/tlsdynamic/.crossbar'
2015-12-24T19:52:49+0100 [Controller  27108] Controller process starting (CPython-EPollReactor) ..
2015-12-24T19:52:49+0100 [Controller  27108] Node configuration loaded from 'config.json'
2015-12-24T19:52:49+0100 [Controller  27108] Node ID 'thinkpad-t430s' set from hostname
2015-12-24T19:52:49+0100 [Controller  27108] Using default node shutdown triggers [u'shutdown_on_worker_exit']
2015-12-24T19:52:49+0100 [Controller  27108] Joined realm 'crossbar' on node management router
2015-12-24T19:52:49+0100 [Controller  27108] Starting Router with ID 'worker1'...
2015-12-24T19:52:49+0100 [Router      27113] Worker process starting (CPython-EPollReactor) ..
2015-12-24T19:52:50+0100 [Controller  27108] Router with ID 'worker1' and PID 27113 started
2015-12-24T19:52:50+0100 [Router      27113] Realm 'realm1' started
2015-12-24T19:52:50+0100 [Controller  27108] Router 'worker1': realm 'realm1' (named 'realm1') started
2015-12-24T19:52:50+0100 [Controller  27108] Router 'worker1': role 'role1' (named 'authenticator') started on realm 'realm1'
2015-12-24T19:52:50+0100 [Controller  27108] Router 'worker1': role 'role2' (named 'backend') started on realm 'realm1'
2015-12-24T19:52:50+0100 [Router      27113] MyAuthenticator: dynamic authenticator registered.
2015-12-24T19:52:50+0100 [Controller  27108] Router 'worker1': component 'component1' started
2015-12-24T19:52:50+0100 [Router      27113] Loading server TLS key from /home/oberstet/scm/crossbario/crossbarexamples/authenticate/tlsdynamic/.crossbar/server.key
2015-12-24T19:52:50+0100 [Router      27113] Loading server TLS certificate from /home/oberstet/scm/crossbario/crossbarexamples/authenticate/tlsdynamic/.crossbar/server.crt
2015-12-24T19:52:50+0100 [Router      27113] Loading server TLS CA certificate from /home/oberstet/scm/crossbario/crossbarexamples/authenticate/tlsdynamic/.crossbar/intermediate.cert.pem
2015-12-24T19:52:50+0100 [Router      27113] Loading server TLS CA certificate from /home/oberstet/scm/crossbario/crossbarexamples/authenticate/tlsdynamic/.crossbar/ca.cert.pem
2015-12-24T19:52:50+0100 [Router      27113] Using secure default TLS ciphers
2015-12-24T19:52:50+0100 [Router      27113] OpenSSL is using most common elliptic curve (prime256v1 / NIST P-256)
2015-12-24T19:52:50+0100 [Router      27113] Site (TLS) starting on 8080
2015-12-24T19:52:50+0100 [Controller  27108] Router 'worker1': transport 'transport1' started
2015-12-24T19:52:50+0100 [Controller  27108] Starting Container with ID 'worker2'...
2015-12-24T19:52:50+0100 [Container   27118] Worker process starting (CPython-EPollReactor) ..
2015-12-24T19:52:50+0100 [Controller  27108] Container with ID 'worker2' and PID 27118 started
2015-12-24T19:52:50+0100 [Container   27118] TLS client using explicit trust (2 certificates)
2015-12-24T19:52:50+0100 [Container   27118] TLS client trust root CA certificate loaded from '/home/oberstet/scm/crossbario/crossbarexamples/authenticate/tlsdynamic/.crossbar/intermediate.cert.pem'
2015-12-24T19:52:50+0100 [Container   27118] TLS client trust root CA certificate loaded from '/home/oberstet/scm/crossbario/crossbarexamples/authenticate/tlsdynamic/.crossbar/ca.cert.pem'
2015-12-24T19:52:50+0100 [Container   27118] Loaded client TLS key from '/home/oberstet/scm/crossbario/crossbarexamples/authenticate/tlsdynamic/.crossbar/client.key'
2015-12-24T19:52:50+0100 [Container   27118] Loaded client TLS certificate from '/home/oberstet/scm/crossbario/crossbarexamples/authenticate/tlsdynamic/.crossbar/client.crt' (cn='client_0', sha256=7E:66:9A:C1:..)
2015-12-24T19:52:50+0100 [Controller  27108] Container 'worker2': component 'component1' started
2015-12-24T19:52:50+0100 [Router      27113] MyAuthenticator.authenticate: realm='realm1', authid='None', subject_cn='client_0', issuer_cn='intermediate_ca', sha1=B6:E5:E6:F2:2A:86:DB:3C:DC:9F:51:42:58:39:9B:14:92:5D:A1:EB
2015-12-24T19:52:50+0100 [Router      27113] MyAuthenticator.authenticate: client accepted.
2015-12-24T19:52:50+0100 [Container   27118] MyBackend: session joined - SessionDetails(realm = realm1, session = 7863814333309942, authid = client_0, authrole = backend, authmethod = tls)
2015-12-24T19:52:50+0100 [Container   27118] MyBackend: procedure add2() registered
```

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

and uses the following configuration attributes relevant to TLS authentication

* `transport.tls.hostname`: The server hostname to verify the server certificate against.
* `transport.tls.key`: The client's private key.
* `transport.tls.certificate`: The client's certificate - this will be used to authenticate the client!
* `transport.tls.ca_certificates`: If this attribute is present, the server cert will be verified against this list of CA certs (instead of being verified using the platform trust anchors - which is the default when this attribute is missing).


## Testing with curl

To test with curl:

```console
oberstet@thinkpad-t430s:~/scm/crossbario/crossbarexamples/authentication/tls/dynamic$ curl --cacert .crossbar/ca.cert.pem --cert .crossbar/client.crt --key .crossbar/client.key https://localhost:8080 | wc -l
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100 13165  100 13165    0     0   588k      0 --:--:-- --:--:-- --:--:--  584k
116
```

If you leave out the `--cacert`, curl no longer accepts the server certificate:


```console
oberstet@thinkpad-t430s:~$ curl -v https://localhost:8080
* Rebuilt URL to: https://localhost:8080/
* Hostname was NOT found in DNS cache
*   Trying 127.0.0.1...
* Connected to localhost (127.0.0.1) port 8080 (#0)
* successfully set certificate verify locations:
*   CAfile: none
  CApath: /etc/ssl/certs
* SSLv3, TLS handshake, Client hello (1):
* SSLv3, TLS handshake, Server hello (2):
* SSLv3, TLS handshake, CERT (11):
* SSLv3, TLS alert, Server hello (2):
* SSL certificate problem: self signed certificate in certificate chain
* Closing connection 0
curl: (60) SSL certificate problem: self signed certificate in certificate chain
More details here: http://curl.haxx.se/docs/sslcerts.html

curl performs SSL certificate verification by default, using a "bundle"
 of Certificate Authority (CA) public keys (CA certs). If the default
 bundle file isn't adequate, you can specify an alternate file
 using the --cacert option.
If this HTTPS server uses a certificate signed by a CA represented in
 the bundle, the certificate verification probably failed due to a
 problem with the certificate (it might be expired, or the name might
 not match the domain name in the URL).
If you'd like to turn off curl's verification of the certificate, use
 the -k (or --insecure) option.
```

If you leave out the `--cert` and `--key` to specify the client certificate to announce and key to use, Crossbar.io will deny the client:

```console
oberstet@thinkpad-t430s:~$ curl --insecure -v https://localhost:8080
* Rebuilt URL to: https://localhost:8080/
* Hostname was NOT found in DNS cache
*   Trying 127.0.0.1...
* Connected to localhost (127.0.0.1) port 8080 (#0)
* successfully set certificate verify locations:
*   CAfile: none
  CApath: /etc/ssl/certs
* SSLv3, TLS handshake, Client hello (1):
* SSLv3, TLS handshake, Server hello (2):
* SSLv3, TLS handshake, CERT (11):
* SSLv3, TLS handshake, Server key exchange (12):
* SSLv3, TLS handshake, Request CERT (13):
* SSLv3, TLS handshake, Server finished (14):
* SSLv3, TLS handshake, CERT (11):
* SSLv3, TLS handshake, Client key exchange (16):
* SSLv3, TLS change cipher, Client hello (1):
* SSLv3, TLS handshake, Finished (20):
* SSLv3, TLS alert, Server hello (2):
* error:14094410:SSL routines:SSL3_READ_BYTES:sslv3 alert handshake failure
* Closing connection 0
curl: (35) error:14094410:SSL routines:SSL3_READ_BYTES:sslv3 alert handshake failure
oberstet@thinkpad-t430s:~$
```
