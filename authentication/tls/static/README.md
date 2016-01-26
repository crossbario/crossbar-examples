# TLS Static Authentication

This uses a client-side TLS certificate to authenticate a WAMP session against a **static list of principals**.

A WAMP router worker is started that

* runs a TLS listening transport
* configures a list of permissible issuing CAs
* configures a list of principals

A container worker is started with a backend component that connects via TLS and presents a TLS client certificate.

The client certificate is first verified against the list of issuing CAs and the then statically authenticated against the list of principals contained in the node configuration.


## How to test

Start Crossbar.io from this directory. You should see log output like the following up to the `"MyBackend: procedure add2() registered"` log message, which indicates that the backend component has successfully authenticated and registered it's backend procedure.

```console
(python279_1)oberstet@thinkpad-t430s:~/scm/crossbario/crossbarexamples/authentication/tls/static$ crossbar start
2016-01-04T15:40:03+0100 [Controller   9659]      __  __  __  __  __  __      __     __
2016-01-04T15:40:03+0100 [Controller   9659]     /  `|__)/  \/__`/__`|__) /\ |__)  |/  \
2016-01-04T15:40:03+0100 [Controller   9659]     \__,|  \\__/.__/.__/|__)/~~\|  \. |\__/
2016-01-04T15:40:03+0100 [Controller   9659]
2016-01-04T15:40:03+0100 [Controller   9659]     Crossbar.io Version: 0.11.2
2016-01-04T15:40:03+0100 [Controller   9659]     Node Public Key: 622b650ebeba8894e1c4db4a93674f5c0061f4523a6898246828d9c93a8432ec
2016-01-04T15:40:03+0100 [Controller   9659]
2016-01-04T15:40:03+0100 [Controller   9659] Running from node directory '/home/oberstet/scm/crossbario/crossbarexamples/authentication/tls/static/.crossbar'
2016-01-04T15:40:03+0100 [Controller   9659] Controller process starting (CPython-EPollReactor) ..
2016-01-04T15:40:03+0100 [Controller   9659] Node configuration loaded from 'config.json'
2016-01-04T15:40:03+0100 [Controller   9659] Node ID 'thinkpad-t430s' set from hostname
2016-01-04T15:40:03+0100 [Controller   9659] Using default node shutdown triggers [u'shutdown_on_worker_exit']
2016-01-04T15:40:03+0100 [Controller   9659] Joined realm 'crossbar' on node management router
2016-01-04T15:40:03+0100 [Controller   9659] Starting Router with ID 'worker1'...
2016-01-04T15:40:04+0100 [Router       9664] Worker process starting (CPython-EPollReactor) ..
2016-01-04T15:40:04+0100 [Controller   9659] Router with ID 'worker1' and PID 9664 started
2016-01-04T15:40:04+0100 [Router       9664] Realm 'realm1' started
2016-01-04T15:40:04+0100 [Controller   9659] Router 'worker1': realm 'realm1' (named 'realm1') started
2016-01-04T15:40:04+0100 [Controller   9659] Router 'worker1': role 'role1' (named 'backend') started on realm 'realm1'
2016-01-04T15:40:04+0100 [Controller   9659] Router 'worker1': role 'role2' (named 'frontend') started on realm 'realm1'
2016-01-04T15:40:04+0100 [Router       9664] Loading server TLS key from /home/oberstet/scm/crossbario/crossbarexamples/authentication/tls/static/.crossbar/server.key
2016-01-04T15:40:04+0100 [Router       9664] Loading server TLS certificate from /home/oberstet/scm/crossbario/crossbarexamples/authentication/tls/static/.crossbar/server.crt
2016-01-04T15:40:04+0100 [Router       9664] Loading server TLS CA certificate from /home/oberstet/scm/crossbario/crossbarexamples/authentication/tls/static/.crossbar/ca.cert.pem
2016-01-04T15:40:04+0100 [Router       9664] Loading server TLS CA certificate from /home/oberstet/scm/crossbario/crossbarexamples/authentication/tls/static/.crossbar/intermediate.cert.pem
2016-01-04T15:40:04+0100 [Router       9664] Using secure default TLS ciphers
2016-01-04T15:40:04+0100 [Router       9664] No OpenSSL DH parameter file set - DH cipher modes will be deactive!
2016-01-04T15:40:04+0100 [Router       9664] OpenSSL is using elliptic curve prime256v1 (NIST P-256)
2016-01-04T15:40:04+0100 [Router       9664] Site (TLS) starting on 8080
2016-01-04T15:40:04+0100 [Controller   9659] Router 'worker1': transport 'transport1' started
2016-01-04T15:40:04+0100 [Controller   9659] Starting Container with ID 'worker2'...
2016-01-04T15:40:04+0100 [Container    9669] Worker process starting (CPython-EPollReactor) ..
2016-01-04T15:40:05+0100 [Controller   9659] Container with ID 'worker2' and PID 9669 started
2016-01-04T15:40:05+0100 [Container    9669] TLS client using explicit trust (2 certificates)
2016-01-04T15:40:05+0100 [Container    9669] TLS client trust root CA certificate loaded from '/home/oberstet/scm/crossbario/crossbarexamples/authentication/tls/static/.crossbar/ca.cert.pem'
2016-01-04T15:40:05+0100 [Container    9669] TLS client trust root CA certificate loaded from '/home/oberstet/scm/crossbario/crossbarexamples/authentication/tls/static/.crossbar/intermediate.cert.pem'
2016-01-04T15:40:05+0100 [Container    9669] Loaded client TLS key from '/home/oberstet/scm/crossbario/crossbarexamples/authentication/tls/static/.crossbar/client.key'
2016-01-04T15:40:05+0100 [Container    9669] Loaded client TLS certificate from '/home/oberstet/scm/crossbario/crossbarexamples/authentication/tls/static/.crossbar/client.crt' (cn='client_0', sha256=7E:66:9A:C1:..)
2016-01-04T15:40:05+0100 [Controller   9659] Container 'worker2': component 'component1' started
2016-01-04T15:40:05+0100 [Container    9669] MyBackend: session joined - SessionDetails(realm=<realm1>, session=1715122213856655, authid=<client_0>, authrole=<backend>, authmethod=tls, authprovider=None)
2016-01-04T15:40:05+0100 [Container    9669] MyBackend: procedure add2() registered
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
                "ca.cert.pem",
                "intermediate.cert.pem"
            ]
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
                    "type": "static",
                    "principals": {
                        "client_0": {
                            "certificate-sha1": "B6:E5:E6:F2:2A:86:DB:3C:DC:9F:51:42:58:39:9B:14:92:5D:A1:EB",
                            "role": "backend"
                        }
                    }
                }
            }
        }
    }
}
```

The transport configuration contains a `auth` item for configuring WAMP authentication methods, and WAMP-TLS is activated by the `tls` item.

In particular, WAMP-TLS in static mode requires a `principals` configuration.

This is a list of elements

```json
"client_0": {
    "certificate-sha1": "B6:E5:E6:F2:2A:86:DB:3C:DC:9F:51:42:58:39:9B:14:92:5D:A1:EB",
    "role": "backend"
}
```

Above says: if a client connects and presents a certifiate of the given fingerprint, the assign it the `authid = client_0` and the `authrole = backend`.

The fingerprint of a certificate can be computed like this:

```console
(python279_1)oberstet@thinkpad-t430s:~/scm/crossbario/crossbarexamples/authentication/tls/static$ openssl x509 -noout -in .crossbar/client.crt -fingerprint -sha1
SHA1 Fingerprint=B6:E5:E6:F2:2A:86:DB:3C:DC:9F:51:42:58:39:9B:14:92:5D:A1:EB
```

Technically, the fingerprint is just the respective hash value computed over the whole certificate file in DER format:

```console
(python279_1)oberstet@thinkpad-t430s:~/scm/crossbario/crossbarexamples/authentication/tls/static$ openssl x509 -in .crossbar/client.crt -outform der | openssl sha1
(stdin)= b6e5e6f22a86db3cdc9f514258399b14925da1eb
```
