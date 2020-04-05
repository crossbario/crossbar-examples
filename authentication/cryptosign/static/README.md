# WAMP-cryptosign static authentication

WAMP-cryptosign using static configuration example.

In a first terminal, start a [Crossbar.io node](.crossbar/config.json) with a WebSocket transport listening
on port 8080:

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
