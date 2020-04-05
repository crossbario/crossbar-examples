# WAMP-cryptosign over TLS authentication

WAMP-cryptosign over TLS authentication example.

In a first terminal, start a [Crossbar.io node](.crossbar/config.json) with a TLS transport listening
on port 8080, and using a [self-signed certificate](.crossbar/client.crt):

```console
make crossbar
```

In a second terminal, start the clients

```console
make clients
``` 

This will run the following clients in series:

* **Twisted** example over TLS, but *without TLS channel binding*: [python client_tx.py](client_tx.py)
* **Twisted** example over TLS and *with "tls-unique" TLS channel binding*: [python client_tx.py --channel_binding="tls-unique"](client_tx.py)
* **asyncio** example over TLS, but *without TLS channel binding*: [python client_aio.py](client_aio.py)
* **asyncio** example over TLS and *with "tls-unique" TLS channel binding*: [python client_aio.py --channel_binding="tls-unique"](client_aio.py)
