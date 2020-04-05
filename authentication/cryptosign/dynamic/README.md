# WAMP-cryptosign with dynamic authentication

WAMP-cryptosign with dynamic authentication, using a custom authenticator.

In a first terminal, start a [Crossbar.io node](.crossbar/config.json) with a transport listening
on port 8080, and running a [custom authenticator](authenticator.py):

```console
make crossbar
```

In a second terminal, start the clients

```console
make clients
``` 

This will run the following clients in series:

* **Twisted** example: [python client_tx.py](client_tx.py)
* **asyncio** example: [python client_aio.py](client_aio.py)
