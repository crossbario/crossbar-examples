import os
from pprint import pformat
from typing import Optional

from twisted.internet.defer import inlineCallbacks
from twisted.internet.task import LoopingCall

from txaio import time_ns
from autobahn.util import hltype, hlval
from autobahn import wamp
from autobahn.wamp.exception import ApplicationError
from autobahn.wamp.types import SessionDetails, CloseDetails, CallDetails, RegisterOptions, PublishOptions
from autobahn.twisted import sleep
from autobahn.twisted.wamp import ApplicationSession


class ExampleBackend(ApplicationSession):

    def __init__(self, config):
        super().__init__(config)
        self._message = 'Hello, world!'
        self._counter = 0
        self._periodic_loop = LoopingCall(self._periodic)

    @inlineCallbacks
    def onJoin(self, details: SessionDetails):
        self.log.info('{func} Session joined with details {details}', func=hltype(self.onJoin), details=details)

        regs = yield self.register(self)
        for reg in regs:
            self.log.info('{reg}', reg=reg)

        # self._periodic_loop.start(10.)

        self.log.info('{func} Ready!', func=hltype(self.onJoin))

    @inlineCallbacks
    def _periodic(self):
        self._counter += 1

        evt = self._counter
        try:
            yield self.publish('eth.pydefi.clock.ba3b1e9f-3006-4eae-ae88-cf5896b36342.on_clock_tick', evt,
                               options=PublishOptions(acknowledge=True))
        except Exception as e:
            if isinstance(e, ApplicationError) and e.error == 'wamp.error.invalid_argument':
                if 'invalid arg type' not in e.args[0]:
                    raise RuntimeError('did not find expected error text in exception!')
            else:
                raise RuntimeError('unexpected exception raised!')
        else:
            raise RuntimeError('invalid publish did not raise!')

        evt = {'counter': self._counter}
        pub = yield self.publish('eth.pydefi.clock.ba3b1e9f-3006-4eae-ae88-cf5896b36342.on_clock_tick', evt,
                                 options=PublishOptions(acknowledge=True))
        self.log.info('{func} published (publication_id={publication_id})', func=hltype(self._periodic),
                      publication_id=hlval(pub.id))

    def onLeave(self, details: CloseDetails):
        self._periodic_loop.stop()
        self._periodic_loop = None

    @wamp.register('com.example.backend.get_time')
    def get_time(self) -> int:
        return time_ns()

    @wamp.register('com.example.backend.add2', check_types=True)
    def add2(self, x: int, y: int) -> int:
        result = x + y
        self.log.info('{func}: {x} + {y} = {result}', func=hltype(self.add2),
                      result=hlval(result), x=hlval(x), y=hlval(y))
        return result

    @inlineCallbacks
    @wamp.register('com.example.backend.slow_square', check_types=True)
    def slow_square(self, x: int, delay: float) -> int:
        result = x * x
        self.log.info('{func}(delay={delay}): {x}^2 = {result}', func=hltype(self.slow_square),
                      delay=hlval(delay), result=hlval(result), x=hlval(x))
        yield sleep(delay)
        return result

    @wamp.register('com.example.backend.get_message', options=RegisterOptions(details=True))
    def get_message(self, details: Optional[CallDetails]) -> str:
        self.log.info('{func}: details={details}', func=hltype(self.get_message),  details=details)
        return self._message

    @inlineCallbacks
    @wamp.register('com.example.backend.set_message', check_types=True, options=RegisterOptions(details=True))
    def set_message(self, message: str, details: Optional[CallDetails]) -> bool:
        if not 10 < len(message) < 100:
            raise ApplicationError('{}.silly_message'.format(self._prefix), 'Your message too silly!', 10, 100)

        if message != self._message:
            old_message = self._message
            self._message = message
            notification = {
                'user': details.caller_authid,
                'old': old_message,
                'new': message,
            }
            yield self.publish('com.example.backend.on_message_changed',
                               notification,
                               options=PublishOptions(acknowledge=True))
            self.log.info('{func}:\n{notification}', func=hltype(self.set_message), notification=pformat(notification))
            return True
        else:
            return False

    @wamp.register('eth.pydefi.clock.ba3b1e9f-3006-4eae-ae88-cf5896b36342.get_clock_address',
                   check_types=True,
                   options=RegisterOptions(details=True))
    def get_clock_address(self, details: Optional[CallDetails]):
        return '0x29B6c56497CA179e9AAFD739BeBded3f23768903'

    @wamp.register('eth.pydefi.'
                   'replica.ba3b1e9f-3006-4eae-ae88-cf5896b36342.'
                   'book.a17f0b45-1ed2-4b1a-9a7d-c112e8cd5d9b.'
                   'get_candle_history',
                   check_types=True,
                   options=RegisterOptions(details=True))
    def get_candle_history(self, period, details: Optional[CallDetails]):
        self.log.info('{func} period={period}, details={details}', func=hltype(self.get_candle_history),
                      period=hlval(period), details=details)
        # trading.Candle
        candle = {
            'period_dur': 10,
            'start_ts': 1654900797173358641,
            'market_oid': os.urandom(16),
            'modified': 1654900797173358641,
            'quantity': 1.,
            'volume': 1.,
            'price_open': 1.,
            'price_close': 1.,
            'price_min': 1.,
            'price_max': 1.,
            'price_avg': 1.,
            'price_var': 1.,
            'price_avg_volw': 1.,
            'price_var_volw': 1.,
        }
        if 5 < period['period_dur'] < 10:
            candle['foobar_invalid'] = 'something'
        elif 0 < period['period_dur'] <= 5:
            candle['price_open'] = 'something'

        return candle
