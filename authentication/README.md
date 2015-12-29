# Crossbar.io Authentication

Authentication is about *identifying* WAMP clients to Crossbar.io. A WAMP session connecting to a **realm** is authenticated under an **authid** and **authrole**. The **authrole** (and the realm) then is the sole information for *authorization* of actions performed by the client (e.g. "Is this client allowed to publish to topic T?").

The subfolders here contain complete examples of the different authentication mechanisms supported by Crossbar.io.

## Overview

### Session and Transport Level Authentication

Authentication mechanisms in WAMP and Crossbar.io can be distinguished regarding the **level** they work at:

* WAMP session level: the mechanism uses a WAMP message exchange at the WAMP session opening handshake (`HELLO`, `CHALLENGE`, `AUTHENTICATE` and `WELCOME` or `ABORT`). These mechanisms can be used over any WAMP transport.
* WAMP transport level: the mechanism works at the message transport _underlying_ the WAMP session level. The WAMP session level is not involved, othere than being informed of the result of the authentication (`authid` and `authrole`).

Notably, working at the **session level**:

1. **WAMP-Ticket** (`ticket`) - [static](ticket/static) / [dynamic](ticket/dynamic), a shared secret ("ticket") based authentication mechanism
2. **WAMP-CRA** (`wampcra`) - [static](wampcra/static) / [dynamic](wampcra/dynamic), a shared secret, challenge-response scheme supporting salting
3. **WAMP-Cryptosign** (`cryptosign`) - [static](cryptosign/static) / [dynamic](cryptosign/dynamic), a public-private key based authentication scheme using Curve25519 elliptic curve cryptography

and working at the **transport level**:

1. **WAMP-Cookie** (`cookie`) [cookie](cookie), a HTTP cookie-based authentication mechanism
2. **WAMP-TLS** (`tls`) - [static](tls/static) / [dynamic](tls/dynamic), TLS client certificate based authentication using x509 certificates

### Static, Dynamic and Database Authentication

Authentication methods in Crossbar.io are available in different flavors, differing in where the authentication credentials are stored (server-side):

1. **static**: the authentication credentials are configured statically in the Crossbar.io node configuration file. This is only feasible when the set of clients to be authenticated is small and fixed.
2. **dynamic**: the authentication credentials are stored outside of Crossbar.io and the router will call into a user provided WAMP procedure during authentication. This is the most flexible variant.
3. **database**: the authentication credentials are stored inside Crossbar.io in a secure, transactional database. The Crossbar.io credential store can be managed via the node management API, and the credential database spans all authentication methods.

> Note: *database authentication* is not yet available. It will be added to the different mechanisms gradually.
