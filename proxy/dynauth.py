# dynamic authenticator setup; see config4.json as well


def _authenticate(realm, authid, details):
    """
    Authenticate something connecting to the backend.

    This should only be other proxy processes. We have access to all
    the "real" front-end credentials the proxy negotiated with the
    "real" client .. so, we could base decisions here on that if we
     want.
    """
    if details['authextra']['proxy_authid'] not in ["user1", "user2"]:
        raise Exception("Unknown user")

    # this is the pubkey for our node (key.pub from .crossbar
    # directory) because the "client" (the proxy process) will use
    # key.priv by default
    return {
        "pubkey": "a1fd4c2c2954b92ef784b4d14442e2eb159cc74040bb59e43e84b3c56719256f",
        "role": "user",
        "authid": details['authextra']['proxy_authid']
    }


def setup(session, details):
    """
    This hook is called because of this stanza from config4.json:

            "components": [
                {
                    "type": "function",
                    "realm": "realm1",
                    "role": "auth",
                    "callbacks": {
                        "join": "dynauth.setup"
                    }
                }
            ]

    ...which configures the method 'dynauth.setup' (this function) as
    the 'on_join' callback. All we have to do here is register our
    authenticator function (we could do more work async if required).
    """
    return session.register(_authenticate, "auth.backend_cryptosign")
