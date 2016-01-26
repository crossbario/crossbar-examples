# Payload Encryption with Crossbar.io

## How to run

Open a first terminal and start Crossbar.io from this directory:

```console
crossbar start
```

> Crossbar.io will log a lot, since WAMP traffic tracing is enabled. This is to demonstrate that with end-to-end encryption enabled, the router cannot read the app payload anymore.

Then, open a second terminal and start the [client2.py](client2.py):

```console
python client2.py
```

This runs a WAMP client connected to above router, **register** a couple of procedures, as well as **subscribe** to some topics.

Now, open a third terminal and start the [client1.py](client1.py):

```console
python client1.py
```

This runs a WAMP client connected to the same router again, **calls** the procedures in client2.py, as well as **publishes** to topics that client2.py subscribed to.

The call arguments, results or errors, as well as event payloads are end-to-end encrypted, and cannot be read in Crossbar.io

The Crossbar.io log will have lines like this

```console
2015-12-29T00:50:05+0100 [Router      13334] >>RX>> WAMP PUBLISH Message (request = 15, topic = com.myapp.hello, args = None, kwargs = None, acknowledge = True, exclude_me = False, exclude = None, eligible = None, disclose_me = True, enc_algo = cryptobox, enc_key = None, enc_serializer = json, payload = +0uiR25DoPlnjina64/T1NxrUFIWtw+qTJznszqd..)
```

for encrypted messages. Here, the router has received ("RX") a WAMP PUBLISH message that was encrypted with algorithm `enc_algo = cryptobox`.

When you see log lines that have `enc_algo = None`, these are WAMP messages received or sent by Crossbar.io which are not encrypted.
