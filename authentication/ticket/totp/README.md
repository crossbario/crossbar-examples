# TOTP Authentication

This examples demonstrates how to authenticate WAMP session using [TOTP](https://en.wikipedia.org/wiki/Time-based_One-time_Password_Algorithm), specified in IETF [RFC6238](https://tools.ietf.org/html/rfc6238).

* For Android, iOS, and Blackberry: [Google Authenticator](https://support.google.com/accounts/answer/1066447?hl=en) and [here](https://play.google.com/store/apps/details?id=com.google.android.apps.authenticator2)
* For Android and iOS: [Duo Mobile](http://guide.duosecurity.com/third-party-accounts)
* For Windows Phone: [Authenticator](https://www.microsoft.com/en-US/store/apps/Authenticator/9WZDNCRFJ3RJ)
* [Yubico Authenticator](https://play.google.com/store/apps/details?id=com.yubico.yubioath)
* [Authenticator for Pebble by Collin Fair](https://github.com/cpfair/pTOTP)

## How to test

In a first terminal, start Crossbar.io:

```console
crossbar start
```

In a second terminal, start a TOTP generator:

```console
python generate.py
```

This will print a series of TOTP values for 2 test principals ("tobias1" and "user1").

You can also use any TOTP compliant generator, with the respective secrets configured:

* `tobias1`: `CACKN3GRF3KQZMEK`
* `user1`: `BKIV3FXPRA67N4Q5`

> Note: the secrets are **not** case-sensitive.

In a third terminal, start the example WAMP client, replacing the `--ticket` value with the current TOTP value shown for the respective `--authid`:

```console
(python279_1)oberstet@thinkpad-t430s:~/scm/crossbario/crossbarexamples/authentication/ticket/totp$ python client.py --authid tobias1 --ticket 750795
2016-01-18T22:07:14+0100 Client session connected.
2016-01-18T22:07:14+0100 WAMP-Ticket challenge received: Challenge(method=ticket, extra={})
2016-01-18T22:07:14+0100 Client session joined: SessionDetails(realm=<realm1>, session=3647944963854882, authid=<tobias1>, authrole=<frontend>, authmethod=ticket, authprovider=dynamic, authextra=None)
2016-01-18T22:07:14+0100 Client session left: CloseDetails(reason=<wamp.close.normal>, message='None')
2016-01-18T22:07:14+0100 Client session disconnected.
2016-01-18T22:07:14+0100 Main loop terminated.
```

**generator.py** outputs SVGQR codes for the principals defined in **authenticator.py**.


## How it works

We use WAMP-Ticket as the authentication mechanism, and use two helper functions provided by AutobahnPython:

* `autobahn.wamp.auth.compute_totp`: compute a current TOTP value from a (secret) seed
* `autobahn.wamp.auth.generate_totp_secret`: generate a new (random) TOTP seed
