# TLS Static Authentication

This example demonstrates a TLS-enabled router transport as well as TLS client certificate using container worker to connect to the transport of the former router worker.

## How to test

> All key material and certificates have been created using the [create-certificates.sh](create-certificates.sh) shell script. You don't need to run this again, as the generated files are contained in this repo.

Start Crossbar.io from this directory. You should see log output similar to this:

```console
(cpy361_1) oberstet@thinkpad-t430s:~/scm/crossbario/crossbar-examples/encryption/tls$ crossbar start
2017-04-17T16:15:21+0200 [Controller  13326]      __  __  __  __  __  __      __     __
2017-04-17T16:15:21+0200 [Controller  13326]     /  `|__)/  \/__`/__`|__) /\ |__)  |/  \
2017-04-17T16:15:21+0200 [Controller  13326]     \__,|  \\__/.__/.__/|__)/~~\|  \. |\__/
2017-04-17T16:15:21+0200 [Controller  13326]
2017-04-17T16:15:21+0200 [Controller  13326] Version:     Crossbar.io COMMUNITY 17.4.1
2017-04-17T16:15:21+0200 [Controller  13326] Public Key:  6b80913970846aee79243aaae5003e9080f5fb3f35668aa726b1fe9eb700514a
2017-04-17T16:15:21+0200 [Controller  13326]
2017-04-17T16:15:21+0200 [Controller  13326] Node starting with personality "community" [crossbar.controller.node.Node]
2017-04-17T16:15:21+0200 [Controller  13326] Running from node directory "/home/oberstet/scm/crossbario/crossbar-examples/encryption/tls/.crossbar"
2017-04-17T16:15:21+0200 [Controller  13326] Node configuration loaded from "/home/oberstet/scm/crossbario/crossbar-examples/encryption/tls/.crossbar/config.json"
2017-04-17T16:15:21+0200 [Controller  13326] Controller process starting [CPython-EPollReactor] ..
2017-04-17T16:15:21+0200 [Controller  13326] No extra node router roles
2017-04-17T16:15:21+0200 [Controller  13326] Using default node shutdown triggers ['shutdown_on_worker_exit']
2017-04-17T16:15:21+0200 [Controller  13326] Configuring node from local configuration ...
2017-04-17T16:15:21+0200 [Controller  13326] Starting 2 workers ...
2017-04-17T16:15:21+0200 [Controller  13326] Router worker "worker-001" starting ..
2017-04-17T16:15:21+0200 [Router      13331] Router worker "worker-001" process 13331 starting on CPython-EPollReactor ..
2017-04-17T16:15:22+0200 [Router      13331] Router worker "worker-001" session 6899280482084546 initializing ..
2017-04-17T16:15:22+0200 [Router      13331] Router worker "worker-001" session ready
2017-04-17T16:15:22+0200 [Controller  13326] Router worker "worker-001" process 13331 started
2017-04-17T16:15:22+0200 [Router      13331] Realm 'realm1' started
2017-04-17T16:15:22+0200 [Controller  13326] Router 'worker-001': realm 'realm-001' (named 'realm1') started
2017-04-17T16:15:22+0200 [Router      13331] role role-001 on realm realm-001 started
2017-04-17T16:15:22+0200 [Controller  13326] Router 'worker-001': role 'role-001' (named 'backend') started on realm 'realm-001'
2017-04-17T16:15:22+0200 [Router      13331] role role-002 on realm realm-001 started
2017-04-17T16:15:22+0200 [Controller  13326] Router 'worker-001': role 'role-002' (named 'frontend') started on realm 'realm-001'
2017-04-17T16:15:22+0200 [Router      13331] Loading server TLS key from /home/oberstet/scm/crossbario/crossbar-examples/encryption/tls/.crossbar/server.key
2017-04-17T16:15:22+0200 [Router      13331] Loading server TLS certificate from /home/oberstet/scm/crossbario/crossbar-examples/encryption/tls/.crossbar/server.crt
2017-04-17T16:15:22+0200 [Router      13331] Loading server TLS CA certificate from /home/oberstet/scm/crossbario/crossbar-examples/encryption/tls/.crossbar/intermediate.cert.pem
2017-04-17T16:15:22+0200 [Router      13331] Loading server TLS CA certificate from /home/oberstet/scm/crossbario/crossbar-examples/encryption/tls/.crossbar/ca.cert.pem
2017-04-17T16:15:22+0200 [Router      13331] Using secure default TLS ciphers
2017-04-17T16:15:22+0200 [Router      13331] OpenSSL is using elliptic curve prime256v1 (NIST P-256)
2017-04-17T16:15:22+0200 [Router      13331] Site (TLS) starting on 8083
2017-04-17T16:15:22+0200 [Controller  13326] Router 'worker-001': transport 'transport-001' started
2017-04-17T16:15:22+0200 [Controller  13326] Container worker "worker-002" starting ..
2017-04-17T16:15:22+0200 [Container   13335] Container worker "worker-002" process 13335 starting on CPython-EPollReactor ..
2017-04-17T16:15:23+0200 [Container   13335] Container worker "worker-002" session 1330437008912949 initializing ..
2017-04-17T16:15:23+0200 [Container   13335] Container worker "worker-002" session ready
2017-04-17T16:15:23+0200 [Controller  13326] Container worker "worker-002" process 13335 started
2017-04-17T16:15:23+0200 [Container   13335] TLS client using explicit trust (2 certificates)
2017-04-17T16:15:23+0200 [Container   13335] TLS client trust root CA certificate loaded from '/home/oberstet/scm/crossbario/crossbar-examples/encryption/tls/.crossbar/ca.cert.pem'
2017-04-17T16:15:23+0200 [Container   13335] TLS client trust root CA certificate loaded from '/home/oberstet/scm/crossbario/crossbar-examples/encryption/tls/.crossbar/intermediate.cert.pem'
2017-04-17T16:15:23+0200 [Container   13335] Loaded client TLS key from '/home/oberstet/scm/crossbario/crossbar-examples/encryption/tls/.crossbar/client.key'
2017-04-17T16:15:23+0200 [Container   13335] Loaded client TLS certificate from '/home/oberstet/scm/crossbario/crossbar-examples/encryption/tls/.crossbar/client.crt' (cn='b'client_0'', sha256=b'0D:67:89:A7:'..)
2017-04-17T16:15:23+0200 [Controller  13326] Container 'worker-002': component 'component-001' started
2017-04-17T16:15:23+0200 [Controller  13326] Local node configuration applied successfully!
2017-04-17T16:15:23+0200 [Container   13335] /home/oberstet/cpy361_1/lib/python3.6/site-packages/service_identity/pyopenssl.py:97: service_identity.exceptions.SubjectAltNameWarning: Certificate has no `subjectAltName`, falling back to check for a `commonName` for now.  This feature is being removed by major browsers and deprecated by RFC 2818.
2017-04-17T16:15:23+0200 [Router      13331] >>>>> session 4724100793485867 JOINED "realm1" >>>>>

{'session': 4724100793485867, 'authid': 'admin', 'authrole': 'backend', 'authmethod': 'wampcra', 'authprovider': 'static', 'transport': {'type': 'websocket', 'protocol': 'wamp.2.cbor.batched', 'peer': 'tcp4:127.0.0.1:52476', 'http_headers_received': {'user-agent': 'AutobahnPython/0.18.2', 'host': 'localhost:8083', 'upgrade': 'WebSocket', 'connection': 'Upgrade', 'pragma': 'no-cache', 'cache-control': 'no-cache', 'sec-websocket-key': 'jY9lJMtDElRPOV+GWIKNXw==', 'sec-websocket-protocol': 'wamp.2.cbor.batched,wamp.2.cbor,wamp.2.msgpack.batched,wamp.2.msgpack,wamp.2.ubjson.batched,wamp.2.ubjson,wamp.2.json.batched,wamp.2.json', 'sec-websocket-version': '13'}, 'http_headers_sent': {}, 'websocket_extensions_in_use': [], 'cbtid': None, 'client_cert': {'md5': '76:6F:46:E8:5E:F6:59:8F:B8:7D:36:11:AE:DC:B3:82', 'sha1': '1D:E9:A9:09:64:CA:8C:68:4E:A5:C1:46:65:EA:2E:43:A2:76:07:B7', 'sha256': '0D:67:89:A7:1C:9B:89:90:99:6B:E0:55:54:79:DE:C5:41:81:3B:AB:D4:18:23:9E:DD:21:66:12:1D:22:1A:AF', 'expired': False, 'hash': 3564778643, 'serial': 4097, 'signature_algorithm': 'sha256WithRSAEncryption', 'version': 2, 'not_before': '20170417141026Z', 'not_after': '20220322141026Z', 'extensions': [{'name': 'basicConstraints', 'value': 'CA:FALSE', 'criticial': False}, {'name': 'nsCertType', 'value': 'SSL Client, S/MIME', 'criticial': False}, {'name': 'nsComment', 'value': 'OpenSSL Generated Client Certificate', 'criticial': False}, {'name': 'subjectKeyIdentifier', 'value': '30:B6:AC:6A:09:1B:21:95:44:2F:BE:17:94:06:83:3D:D5:BD:ED:E4', 'criticial': False}, {'name': 'authorityKeyIdentifier', 'value': 'keyid:BB:E8:E4:51:04:82:74:54:E9:DB:70:D8:90:36:28:08:E7:A6:FF:A3\n', 'criticial': False}, {'name': 'keyUsage', 'value': 'Digital Signature, Non Repudiation, Key Encipherment', 'criticial': True}, {'name': 'extendedKeyUsage', 'value': 'TLS Web Client Authentication, E-mail Protection', 'criticial': False}], 'subject': {'c': 'DE', 'st': 'Bavaria', 'l': 'Erlangen', 'o': 'Crossbar.io GmbH', 'cn': 'client_0'}, 'issuer': {'c': 'DE', 'st': 'Bavaria', 'o': 'Crossbar.io GmbH', 'cn': 'intermediate_ca'}}, 'channel_id': '30d1acac8e05e812ec838397e53782be2cb30d4feb3260a764bd8f2476ec3ba0'}}

2017-04-17T16:15:23+0200 [Container   13335] connected! SessionDetails(realm=<realm1>, session=4724100793485867, authid=<admin>, authrole=<backend>, authmethod=wampcra, authprovider=static, authextra=None, resumed=None, resumable=None, resume_token=None)
2017-04-17T16:15:23+0200 [Container   13335] ok, subscribed to topic com.example.topic1
2017-04-17T16:15:23+0200 [Container   13335] ok, subscribed to topic com.foobar.topic1
2017-04-17T16:15:23+0200 [Container   13335] ok, subscribed to topic com.foobar.topic2
2017-04-17T16:15:23+0200 [Container   13335] procedure add2() registered
```

----

To also demonstrate how a development/self-signed situation can also
work, this example creates its own root and intermediate certificate
authorities with the "create-certificates.sh" script -- normally these
would be "real" authorities (and you'd pay someone money for the
server-side certificate and the client-side certificate).

The output from ./create-certificates.sh is included already in the
.crossbar configuration for convenience only but you can re-run it if
you like to (re-)generate the example certificates from scratch.

./create-certificates.sh does the following:

 1. creates a self-signed root certificate-authority cert
 2. creates an intermediate authority signed by the cert in 1
 3. creates a server-side certificate signed by the intermediate (2)
 4. creatse a client-side certificate signed by the intermediate (2)
 5. creates a 'dhparam' file

In a "real world" scenario, the certificates from 1 and 2 would be an
actual certificate authority of course. In such a case you would not
normally need to include the 'ca_certificates' lines in the crossbar
config (if your certificate authority's root is usually trused by
browsers). However, you can still include them giving additional
security.


To use this same example, but turn *off* the requirement for a
client-side certificate, change the server endpoint configuration to:

    "tls": {
        "certificate": "server.crt",
        "key": "server.key",
        "dhparam": "dhparam"
    }

...and the client endpoint configuration to:

     "tls": {
         "hostname": "localhost",
         "ca_certificates": [
             "ca.cert.pem",
             "intermediate.cert.pem"
         ]
     }

The "ca_certificates" is required for the client because the server is
using a certificate chain that is not normally trusted by any client
-- if this were a "real" certificate, you would just need
``"hostname": "localhost"`` on the client side.

On the server side, the lack of a ``ca_certificates`` key indicates
that we don't care if the client is using a certificate at all (nor
what CA may be the root of that cert).
