# Crossbar.io Authentication

Crossbar.io offers a range of authentication methods. There are working code examples for these in this repo:

1. **WAMP-Anonymous** (`anonymous`) - [static](anonymous/static) / [dynamic](anonymous/dynamic) / [function](anonymous/function), anonymous "authentication" (the client isn't actually identifying itself)
2. **WAMP-Ticket** (`ticket`) - [static](ticket/static) / [dynamic](ticket/dynamic) / [function](ticket/function), a shared secret ("ticket") based authentication mechanism
3. **WAMP-CRA** (`wampcra`) - [static](wampcra/static) / [dynamic](wampcra/dynamic) / [function](wampcra/function), a shared secret, challenge-response scheme supporting salting
4. **WAMP-SCRAM** (`scram`) - [static](scram/static) / [dynamic](scram/dynamic) / [function](scram/function), a shared secret, challenge-response scheme supporting salting and more advanced options (better security properties compared to WAMP-CRA)
5. **WAMP-Cryptosign** (`cryptosign`) - [static](cryptosign/static) / [dynamic](cryptosign/dynamic) / [function](cryptosign/function), a public-private key based authentication scheme using Curve25519 elliptic curve cryptography
6. **WAMP-TLS** (`tls`) - [static](tls/static) / [dynamic](tls/dynamic) / [function](tls/function), TLS client certificate based authentication using x509 certificates
7. **WAMP-Cookie** (`cookie`) [cookie](cookie), a HTTP cookie-based authentication mechanism

## Static, Dynamic and Function-based Authentication

For the above examples, the

* `static` folders contain examples where the credentials are configured statically in the Crossbar.io config
* `dynamic` folders contain examples where authentication is handled by an authenticator WAMP component (which is called at run-time via WAMP RPC)
* `function` folders contain examples where authentication is handled by an authenticator (Python) function (which is called at run-time via Python function call)

## Status

Method | Static | Dynamic | Function
-- | -- | -- | --
Anonymous | OK | OK | FIXME
Ticket | OK | OK | OK
CRA | OK | OK | OK
SCRAM | FIXME | FIXME | FIXME
Cryptosign | OK | OK | OK
TLS | FIXME | FIXME | FIXME
Cookie | FIXME | FIXME | FIXME

## More

Then there is

* [totp](ticket/totp), which is using WAMP-Ticket to implement [TOTP](https://en.wikipedia.org/wiki/Time-based_One-time_Password_Algorithm) based authentication

and

* [advanced](advanced), which shows how to run dynamic authenticators in dedicated realms, and how to let dynamic authenticators redirect clients to specific realms

