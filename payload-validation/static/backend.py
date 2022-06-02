from pprint import pformat
from typing import Optional
from twisted.internet.defer import inlineCallbacks
from txaio import time_ns
from autobahn.util import hltype, hlval
from autobahn import wamp
from autobahn.wamp.exception import ApplicationError
from autobahn.wamp.types import SessionDetails, CallDetails, RegisterOptions, PublishOptions
from autobahn.twisted import sleep
from autobahn.twisted.wamp import ApplicationSession


class ExampleBackend(ApplicationSession):

    def __init__(self, config):
        super().__init__(config)
        self._message = 'Hello, world!'

    @inlineCallbacks
    def onJoin(self, details: SessionDetails):
        self.log.info('{func} Session joined with details {details}', func=hltype(self.onJoin), details=details)

        regs = yield self.register(self)
        for reg in regs:
            self.log.info('{reg}', reg=reg)

        self.log.info('{func} Ready!', func=hltype(self.onJoin))

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
        # Candle
        result = {}
        return result
