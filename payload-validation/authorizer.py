from pprint import pformat
from uuid import UUID
from twisted.internet.defer import inlineCallbacks

from autobahn.util import hltype, hlval
from autobahn.twisted.wamp import ApplicationSession
from autobahn.wamp.uri import Pattern


class ExampleAuthorizer(ApplicationSession):

    def __init__(self, config):
        super().__init__(config)
        self._prefix = 'com.example.private'
        self._pattern1 = Pattern('{}.clock.<clock:str>.<rest:str>'.format(self._prefix), Pattern.URI_TARGET_ENDPOINT)
        self._pattern2 = Pattern('{}.replica.<replica:str>.book.<book:str>.get_candle_history'.format(self._prefix),
                                 Pattern.URI_TARGET_ENDPOINT)

    @inlineCallbacks
    def onJoin(self, details):
        yield self.register(self.authorize, 'com.example.internal.authorize')
        self.log.info('{func} ok, ready!', func=hltype(self.onJoin))

    def authorize(self, session, uri, action, options):
        authorization = None

        if (session['authrole'] == 'frontend' and
                uri.startswith('{}.clock.'.format(self._prefix)) and action in ['call', 'subscribe']):
            try:
                args, kwargs = self._pattern1.match(uri)
                if 'clock' in kwargs:
                    _clock_oid = str(UUID(kwargs['clock']))
                else:
                    _clock_oid = None
            except ValueError as e:
                raise RuntimeError('could not parse "clock" UUID from URI "{}": {}'.format(uri, e))
            else:
                if action == 'call' and uri.endswith('.get_clock_address'):
                    authorization = {
                        'allow': True,
                        'disclose': False,
                        'cache': True,
                        'validate': {
                            'call_result': 'Address',
                            'meta': {
                                'kwargs': {
                                    'clock_oid': _clock_oid
                                }
                            }
                        }
                    }
                elif action in ['event'] and uri.endswith('.on_clock_tick'):
                    authorization = {
                        'allow': True,
                        'disclose': False,
                        'cache': True,
                        'validate': {
                            'event': 'trading.ClockTickSigned',
                            'extra': {
                                'clock_oid': _clock_oid
                            }
                        }
                    }

        elif (session['authrole'] == 'frontend' and
              uri.startswith('{}.replica.'.format(self._prefix)) and action in ['call']):
            try:
                # match
                # com.example.private.replica.<replica:str>                       .book.<book:str>                          .get_candle_history
                # com.example.private.replica.ba3b1e9f-3006-4eae-ae88-cf5896b36342.book.a17f0b45-1ed2-4b1a-9a7d-c112e8cd5d9b.get_candle_history
                args, kwargs = self._pattern2.match(uri)
                if 'replica' in kwargs:
                    _replica_oid = str(UUID(kwargs['replica']))
                else:
                    _replica_oid = None
                if 'book' in kwargs:
                    _book_oid = str(UUID(kwargs['book']))
                else:
                    _book_oid = None
            except ValueError as e:
                raise RuntimeError('could not parse "replica" and "book" UUIDs from URI "{}": {}'.format(uri, e))
            else:
                if action == 'call' and uri.endswith('.get_candle_history'):
                    authorization = {
                        'allow': True,
                        'disclose': False,
                        'cache': True,
                        'validate': {
                            'call': 'trading.Period',
                            'call_result': 'trading.CandleResult',
                            'call_error': 'trading.ErrorInvalidPeriod',
                            'extra': {
                                'replica_oid': _replica_oid,
                                'book_oid': _book_oid,
                            }
                        }
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
