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
        self._prefix = 'com.example.backend.'

    @inlineCallbacks
    def onJoin(self, details: SessionDetails):
        self.log.info('{func} Session joined with details {details}', func=hltype(self.onJoin), details=details)

        regs = yield self.register(self, prefix=self._prefix)
        for reg in regs:
            self.log.info('{reg}', reg=reg)

        self.log.info('{func} Ready!', func=hltype(self.onJoin))

    @wamp.register('get_time')
    def get_time(self) -> int:
        return time_ns()

    @wamp.register('add2', check_types=True)
    def add2(self, x: int, y: int) -> int:
        result = x + y
        self.log.info('{func}: {x} + {y} = {result}', func=hltype(self.add2),
                      result=hlval(result), x=hlval(x), y=hlval(y))
        return result

    @inlineCallbacks
    @wamp.register('slow_square', check_types=True)
    def slow_square(self, x: int, delay: float) -> int:
        yield sleep(delay)
        return x * x

    @wamp.register('get_message', options=RegisterOptions(details=True))
    def get_message(self, details: Optional[CallDetails]) -> str:
        self.log.info('{func}: details={details}', func=hltype(self.get_message),  details=details)
        return self._message

    @inlineCallbacks
    @wamp.register('set_message', check_types=True, options=RegisterOptions(details=True))
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
            yield self.publish('{}on_message_changed'.format(self._prefix),
                               notification,
                               options=PublishOptions(acknowledge=True))
            self.log.info('{func}:\n{notification}', func=hltype(self.set_message), notification=pformat(notification))
            return True
        else:
            return False
