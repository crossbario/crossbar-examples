# Crossbar.io Authentication

Crossbar.io offers a range of authentication methods. There are working code examples for these in this repo:

1. **WAMP-Anonymous** (`anonymous`) - [static](anonymous/static) / [dynamic](anonymous/dynamic), anonymous "authentication" (the client isn't actually identifying itself)
2. **WAMP-Ticket** (`ticket`) - [static](ticket/static) / [dynamic](ticket/dynamic), a shared secret ("ticket") based authentication mechanism
3. **WAMP-CRA** (`wampcra`) - [static](wampcra/static) / [dynamic](wampcra/dynamic), a shared secret, challenge-response scheme supporting salting
4. **WAMP-Cryptosign** (`cryptosign`) - [static](cryptosign/static) / [dynamic](cryptosign/dynamic), a public-private key based authentication scheme using Curve25519 elliptic curve cryptography
5. **WAMP-Cookie** (`cookie`) [cookie](cookie), a HTTP cookie-based authentication mechanism
6. **WAMP-TLS** (`tls`) - [static](tls/static) / [dynamic](tls/dynamic), TLS client certificate based authentication using x509 certificates

Then there is

* [totp](ticket/totp), which is using WAMP-Ticket to implement [TOTP](https://en.wikipedia.org/wiki/Time-based_One-time_Password_Algorithm) based authentication

and

* [advanced](advanced), which shows how to run dynamic authenticators in dedicated realms, and how to let dynamic authenticators redirect clients to specific realms

## Static, Dynamic and Database Authentication

For the above examples, the

* `static` folder contains examples where the credentials are stored in the Crossbar.io config
* `dynamic` folder contains an examples where authentication is handled by an authenticator component (which may store the credentials itself or serve as a connector to an existing authentication mechanism/credentials store)
