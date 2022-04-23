import os
from pprint import pprint, pformat

import txaio
txaio.use_twisted()

from txaio import make_logger

from twisted.internet.defer import inlineCallbacks

from autobahn.twisted.wamp import ApplicationSession
from autobahn.wamp.exception import ApplicationError
from autobahn.util import hl, hltype, hlid, hlval

MYTICKET = os.environ.get('MYTICKET', None)

# our principal "database"
PRINCIPALS_DB = {
   "joe": {
      "ticket": "secret!!!",
      "role": "frontend"
   },
   "client2": {
      "ticket": "123sekret",
      "role": "frontend"
   },
   "client1": {
      "ticket": MYTICKET,
      "role": "frontend"
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
        ticket = details['ticket']
        print("WAMP-Ticket dynamic authenticator invoked: realm='{}', authid='{}', ticket='{}'".format(realm, authid, ticket))
        pprint(details)

        if authid in PRINCIPALS_DB:
            if ticket == PRINCIPALS_DB[authid]['ticket']:
                return PRINCIPALS_DB[authid]['role']
            else:
                raise ApplicationError("com.example.invalid_ticket", "could not authenticate session - invalid ticket '{}' for principal {}".format(ticket, authid))
        else:
            raise ApplicationError("com.example.no_such_user", "could not authenticate session - no such principal {}".format(authid))

    return authenticate
