# TLS Static Authentication

This uses a client-side TLS certificate to verify the connection to a server.


Note that we're still


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
