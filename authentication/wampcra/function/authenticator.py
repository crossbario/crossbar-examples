import os
from pprint import pprint, pformat

import txaio
txaio.use_twisted()

from txaio import make_logger

from twisted.internet.defer import inlineCallbacks

from autobahn.twisted.wamp import ApplicationSession
from autobahn.wamp.exception import ApplicationError
from autobahn.xbr._util import hlval, hlid, hl, hltype


# our user "database"
USERDB = {
    'client1': {
        # these are required:
        'secret': 'secret123',  # the secret/password to be used
        'role': 'frontend'    # the auth role to be assigned when authentication succeeds
    },
    'joe': {
        # these are required:
        'secret': 'secret2',  # the secret/password to be used
        'role': 'frontend'    # the auth role to be assigned when authentication succeeds
    },
    'hans': {
        'authid': 'ID09125',  # assign a different auth ID during authentication
        'secret': '123456',
        'role': 'frontend'
    },
    'peter': {
        # use salted passwords

        # autobahn.wamp.auth.derive_key(secret.encode('utf8'), salt.encode('utf8')).decode('ascii')
        'secret': 'prq7+YkJ1/KlW1X0YczMHw==',
        'role': 'frontend',
        'salt': 'salt123',
        'iterations': 100,
        'keylen': 16
    }
}


log = make_logger()


async def create_authenticator(config, controller):
    """
    Creates and returns a function to do authentication. The actual
    authentication method will be called like:

        authenticate(realm, authid, session_details)

    Note that this function can itself do async work (as can the
    "authenticate" method). For example, we could connect to a
    database here (and then use that connection in the authenticate()
    method)

    'controller' will be None unless `"expose_controller": true` is in
    the config.
    """
    log.info(
        'create_authenticator(config={config}) {func}',
        config=pformat(config),
        func=hltype(create_authenticator),
    )

    def authenticate(realm, authid, details):
        print("WAMP-CRA dynamic authenticator invoked: realm='{}', authid='{}'".format(realm, authid))
        pprint(details)

        if authid in USERDB:
            # return a dictionary with authentication information ...
            return USERDB[authid]
        else:
            raise ApplicationError('com.example.no_such_user', 'could not authenticate session - no such user {}'.format(authid))

    return authenticate
