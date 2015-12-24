# Crossbar.io Authentication Mechanisms

The subfolders here contain complete examples of the different authentication mechanisms supported by Crossbar.io.

Notably, working at the **WAMP level**:

1. **Ticket** (`ticket`) - [static](ticket) / [dynamic](ticketdynamic), a shared secret ("ticket") based authentication mechanism
2. **WAMP-CRA** (`wampcra`) - [static](wampcra) / [dynamic](wampcradynamic), a shared secret, challenge-response scheme supporting salting
3. **Ed25519** (`ed25519`) - [static](ed25519) / [dynamic](ed25519dynamic), a public-private key based authentication scheme using Curve25519 elliptic curve cryptography

and working at the **Transport level**:

1. **Cookie** (`cookie`) [auto](cookie), a HTTP cookie-based authentication mechanism
2. **TLS** (`tls`) - [static](tls) / [dynamic](tlsdynamic), TLS client certificate based authentication using x509 certificates
