# Dynamic authenticators: advanced features

## Running authenticators in configurable realms

By default, dynamic authenticators must run in the same realm as the session that is connecting.

In some situations, this can be a pain, and it is possible to invoke dynamic authenticators on a different realm than the session connecting by configuring an explicit realm:

```json
"auth": {
   "ticket": {
      "type": "dynamic",
      "authenticator": "com.example.authenticate",
      "authenticator-realm": "realm-auth"
   }
}
```

Here, we have configured WAMP-Ticket with a dynamic authenticator by not only providing the URI of the procedure to be called ("com.example.authenticate"), but also the realm on which to invoke said procedure ("realm-auth").

The authenticator component lives on the "realm-auth" realm:

```json
{
   "type": "class",
   "classname": "authenticator.AuthenticatorSession",
   "realm": "realm-auth",
   "role": "authenticator"
}
```

Here is how to test with this example. Start Crossbar.io in a first terminal. Then start the client in a second terminal:

```console
python client.py --realm realm-user1 --authid user1
```

The session will be authenticated by the authenticator running on a different realm than the connecting session.


## Automatic realm selection

By default, clients must connect and announce the realm they want to join.

In some situations, it can be nice to have a dynamic authenticator also choose the right realm the session should be joined on.

Here is how to test with this example. Start Crossbar.io in a first terminal. Then start the client in a second terminal:

```console
python client.py --authid user1
```

The client will be joined automatically to realm "realm-user1".

Try starting the client like this:

```console
python client.py --authid user2
```

You'll notice the client will now be joined to realm "realm-user2" instead.

