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

## Test

To run all examples, start the script [test_all.sh](test_all.sh):

```
(cpy39_1) (base) oberstet@intel-nuci7:~/scm/crossbario/crossbar-examples/authentication$ ./test_all.sh
...
Mi 13. Apr 19:03:10 CEST 2022

Crossbar.io WAMP Authentication Test Summary:
=============================================

wamp-cryptosign-static-tx-good:              OK
wamp-cryptosign-static-tx-bad:               OK
wamp-cryptosign-static-tx-noauthid-good:     OK
wamp-cryptosign-static-tx-noauthid-bad:      OK
wamp-cryptosign-static-aio-good:             OK
wamp-cryptosign-static-aio-bad:              OK
wamp-cryptosign-static-aio-noauthid-good:    OK
wamp-cryptosign-static-aio-noauthid-bad:     OK
wamp-cryptosign-tls-tx-cnlbin-none-good:     OK
wamp-cryptosign-tls-tx-cnlbin-none-bad:      OK
wamp-cryptosign-tls-tx-cnlbin-unique-good:   OK
wamp-cryptosign-tls-tx-cnlbin-unique-bad:    OK
wamp-scram-tx-good:                          OK
wamp-scram-tx-bad:                           FAIL
wamp-ticket-static-good:                     OK
wamp-ticket-static-bad:                      OK
wamp-ticket-dynamic-good:                    OK
wamp-ticket-dynamic-bad:                     OK
wamp-ticket-function-good:                   OK
wamp-ticket-function-bad:                    OK
wamp-tls-static-cnlbind-unique-good:         OK
wamp-tls-static-cnlbind-unique-bad:          OK
wamp-cra-static-good:                        OK
wamp-cra-static-bad:                         OK
wamp-cra-dynamic-good:                       OK
wamp-cra-dynamic-bad:                        OK
wamp-cra-function-good:                      OK
wamp-cra-function-bad:                       OK
```

### Tests Structure

1. authentication: `anonymous`, `ticket`, `wampcra`, `scram`, `cryptosign`, `cookie`
2. client credentials: `good`, `bad`
3. client framework: `tx`, `aio`
4. client API: `apprun`, `comp`
5. router authenticator: `static`, `dynamic`
6. router TLS: `plain`, `tls`, `tls-unique`
7. router setup: `rtr`, `pxy-rtr`

> These are potentially 6*2*2*2*2*3*2 == 576 test combinations!

## More

Then there is

* [totp](ticket/totp), which is using WAMP-Ticket to implement [TOTP](https://en.wikipedia.org/wiki/Time-based_One-time_Password_Algorithm) based authentication

and

* [advanced](advanced), which shows how to run dynamic authenticators in dedicated realms, and how to let dynamic authenticators redirect clients to specific realms

