from pprint import pformat
from uuid import UUID
from twisted.internet.defer import inlineCallbacks

from autobahn.util import hltype, hlval
from autobahn.twisted.wamp import ApplicationSession
from autobahn.wamp.uri import Pattern


class ExampleAuthorizer(ApplicationSession):

    def __init__(self, config):
        super().__init__(config)
        self._pattern1 = Pattern('eth.pydefi.clock.<clock:str>.<rest:str>', Pattern.URI_TARGET_ENDPOINT)
        self._pattern2 = Pattern('eth.pydefi.replica.<replica:str>.book.<book:str>.get_candle_history',
                                 Pattern.URI_TARGET_ENDPOINT)

    @inlineCallbacks
    def onJoin(self, details):
        yield self.register(self.authorize, 'com.example.authorize')
        self.log.info('{func} ok, ready!', func=hltype(self.onJoin))

    def authorize(self, session, uri, action, options):
        authorization = None

        if (session['authrole'] == 'frontend' and uri.startswith('com.example.backend.') and
                action in ['call', 'subscribe']):
            authorization = {
                'allow': True,
                'cache': True,  # optional
                'disclose': True,  # optional
            }

        elif (session['authrole'] == 'frontend' and uri.startswith('eth.pydefi.clock.') and
              action in ['call', 'subscribe']):
            try:
                # match
                # eth.pydefi.clock.<clock:str>.get_clock_address
                # eth.pydefi.clock.ba3b1e9f-3006-4eae-ae88-cf5896b36342.get_clock_address
                args, kwargs = self._pattern1.match(uri)
                if 'clock' in kwargs:
                    _clock_oid = str(UUID(kwargs['clock']))
                else:
                    _clock_oid = None
            except ValueError:
                pass
            else:
                if action == 'call' and uri.endswith('.get_clock_address'):
                    validate = {
                        'catalog': 'pydefi.eth',
                        'interface': '81256d9b-1e0a-434c-aa75-9cc0dfe8e1ea',
                        'procedure': 'get_clock_address',
                        'args': None,
                        'kwargs': None,
                        'results': ['Address'],
                        'kwresults': None,
                    }
                elif action == 'subscribe' and uri.endswith('.on_clock_tick'):
                    validate = {
                        'catalog': 'pydefi.eth',
                        'interface': '81256d9b-1e0a-434c-aa75-9cc0dfe8e1ea',
                        'topic': 'on_clock_tick',
                        'args': ['trading.ClockTickSigned'],
                        'kwargs': None,
                        'results': None,
                        'kwresults': None,
                    }
                else:
                    validate = None

                authorization = {
                    'allow': True,
                    'disclose': False,
                    'meta': {
                        'args': None,
                        'kwargs': {
                            'clock_oid': _clock_oid
                        }
                    },
                    'validate': validate,
                    'cache': True,
                }

        elif (session['authrole'] == 'frontend' and uri.startswith('eth.pydefi.replica.') and
              action in ['call', 'subscribe']):
            try:
                # match
                # eth.pydefi.replica.<replica:str>.book.<book:str>.get_candle_history
                # eth.pydefi.replica.ba3b1e9f-3006-4eae-ae88-cf5896b36342.book.a17f0b45-1ed2-4b1a-9a7d-c112e8cd5d9b.get_candle_history
                args, kwargs = self._pattern2.match(uri)
                if 'replica' in kwargs:
                    _replica_oid = str(UUID(kwargs['replica']))
                else:
                    _replica_oid = None
                if 'book' in kwargs:
                    _book_oid = str(UUID(kwargs['book']))
                else:
                    _book_oid = None
            except ValueError:
                pass
            else:
                if action == 'call' and uri.endswith('.get_candle_history'):
                    validate = {
                        'catalog': 'pydefi.eth',
                        'interface': '6563cfac-498c-47cd-9ff1-24cbd0bdc6e5',
                        'procedure': 'get_candle_history',
                        'args': ['trading.Period'],
                        'kwargs': None,
                        'results': ['trading.Candle'],
                        'kwresults': None,
                    }
                else:
                    validate = None

                authorization = {
                    'allow': True,
                    'disclose': False,
                    'meta': {
                        'args': None,
                        'kwargs': {
                            'replica_oid': _replica_oid,
                            'book_oid': _book_oid,
                        }
                    },
                    'validate': validate,
                    'cache': True,
                }

        if authorization:
            self.log.info('{func}: authrole="{authrole}", uri="{uri}", action="{action}" -> '
                          'ALLOW with authorization=\n{authorization}',
                          func=hltype(self.authorize),
                          authrole=hlval(session['authrole']),
                          uri=hlval(uri),
                          action=hlval(action),
                          authorization=pformat(authorization))
            return authorization
        else:
            self.log.info('{func}: authrole="{authrole}", uri="{uri}", action="{action}" -> DENY',
                          func=hltype(self.authorize),
                          authrole=hlval(session['authrole']),
                          uri=hlval(uri),
                          action=hlval(action))
            return False
