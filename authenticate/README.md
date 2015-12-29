# Crossbar.io Authentication

The subfolders here contain complete examples of the different authentication mechanisms supported by Crossbar.io.

## Overview

Authentication mechanisms in WAMP can be distinguished regarding the **level** they work at:

* WAMP session level: the mechanism uses a WAMP message exchange at the WAMP session opening handshake (`HELLO`, `CHALLENGE`, `AUTHENTICATE` and `WELCOME` or `ABORT`). These mechanisms can be used over any WAMP transport.
* WAMP transport level: the mechanism works at the message transport _underlying_ the WAMP session level. The WAMP session level is not involved, othere than being informed of the result of the authentication (`authid` and `authrole`).

Notably, working at the **session level**:

1. **WAMP-Ticket** (`ticket`) - [static](ticket) / [dynamic](ticketdynamic), a shared secret ("ticket") based authentication mechanism
2. **WAMP-CRA** (`wampcra`) - [static](wampcra) / [dynamic](wampcradynamic), a shared secret, challenge-response scheme supporting salting
3. **WAMP-Cryptosign** (`cryptosign`) - [static](cryptosign) / [dynamic](cryptosigndynamic), a public-private key based authentication scheme using Curve25519 elliptic curve cryptography

and working at the **transport level**:

1. **WAMP-Cookie** (`cookie`) [auto](cookie), a HTTP cookie-based authentication mechanism
2. **WAMP-TLS** (`tls`) - [static](tls) / [dynamic](tlsdynamic), TLS client certificate based authentication using x509 certificates
