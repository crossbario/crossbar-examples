import sys
import argparse

import txaio
txaio.use_twisted()

from autobahn.twisted.component import Component, run
from autobahn.wamp.types import RegisterOptions
from autobahn.wamp.exception import ApplicationError
from twisted.internet.defer import inlineCallbacks


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--debug', dest='debug', action='store_true',
                        default=False, help='Enable logging at level "debug".')
    parser.add_argument('--url', dest='url', type=str, default='ws://localhost:8080/ws',
                        help='The router URL (default: ws://localhost:8080/ws).')
    parser.add_argument('--realm', dest='realm', type=str, default="realm1",
                        help='The realm to join. If not provided, let the router auto-choose the realm.')
    parser.add_argument('--authid', dest='authid', type=str, default="foobar@example.com",
                        help='The authid to connect under. If not provided, let the router auto-choose the authid.')
    parser.add_argument('--password', dest='password', type=str,
                        help='The password to use.')
    options = parser.parse_args()

    if options.debug:
        txaio.start_logging(level='debug')
    else:
        txaio.start_logging(level='info')

    extra = {
        'exit_details': None,
    }
    print("Connecting to {}: requesting realm={}, authid={}".format(
        options.url, options.realm, options.authid))

    # foobar@example.com => secret123
    # https://github.com/crossbario/autobahn-python/blob/master/autobahn/wamp/test/test_wamp_scram.py
    component = Component(
        transports=options.url,
        realm=options.realm,
        authentication={
            "scram": {
                "authid": options.authid,
                "password": options.password,
                "kdf": "argon2id13",
                'iterations': 4096,
                'memory': 512,
            }
        }
    )

    @component.on_join
    def _on_join(session, details):
        print("Session joined: {}".format(details))
        session.leave()

    @component.on_leave
    def _on_leave(session, details):
        print("Session left: {}".format(details))
        extra['exit_details'] = details
        component.stop()
        session.disconnect()

    @component.on_disconnect
    def _on_disconnect(session, was_clean):
        print("Session disconnected: {}".format(was_clean))

    run([component], log_level='debug' if options.debug else 'info')

    # CloseDetails(reason=<wamp.error.not_authorized>, message='WAMP-CRA signature is invalid')
    print("Session ended: {}".format(extra['exit_details']))

    if not extra['exit_details'] or extra['exit_details'].reason != 'wamp.close.normal':
        sys.exit(1)
    else:
        sys.exit(0)
