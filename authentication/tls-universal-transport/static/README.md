# One TLS port, three protocols: the universal transport

A Crossbar.io router with a single listening transport of type `universal` on port
8080, over TLS. The router tells the protocols apart on each connection:

* **HTTP(S)**: the static files in [`web/`](web/), served without authentication;
* **WAMP over WebSocket**, at path `/ws`, authenticated with WAMP-Cryptosign;
* **WAMP over RawSocket**, on the same port, authenticated with WAMP-Cryptosign.

Static content is public; only WAMP sessions authenticate. That is a common
deployment: a web application whose pages anyone may load, and whose WAMP backend
admits only known clients.

The realm, the role and the two Cryptosign principals are the ones of
[`../../cryptosign/tls`](../../cryptosign/tls). The TLS server key and certificate in
`.crossbar/` are a self-signed pair for `localhost` (valid until 2036). All of it is
published test material, for trying the example, never for production.

## Run

Start the router from this directory:

```console
crossbar start
```

Fetch the page, trusting exactly the router's self-signed certificate:

```console
curl --cacert .crossbar/server.crt https://localhost:8080/
```

Connect a WAMP client, over WebSocket or over RawSocket, with a Cryptosign key of the
`cryptosign/tls` example (`client.py` trusts exactly `.crossbar/server.crt`):

```console
python client.py --transport websocket --key ../../cryptosign/tls/.keys/client01.key
python client.py --transport rawsocket --key ../../cryptosign/tls/.keys/client01.key
```

Both join the realm `devices` as `client01@example.com`. A key that belongs to no
principal is refused (`wamp.error.not_authorized`), and so is a client that offers no
authentication (`python client.py`, anonymous: `wamp.error.no_auth_method`). There is
no anonymous WAMP access on either transport; only the web pages are public.
