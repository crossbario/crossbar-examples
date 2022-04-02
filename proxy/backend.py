import math

from twisted.internet.defer import inlineCallbacks

from autobahn.twisted.util import sleep
from autobahn.twisted.wamp import ApplicationSession
from autobahn.wamp.exception import ApplicationError
from autobahn.wamp.types import CallResult


class MyBackend(ApplicationSession):

    @inlineCallbacks
    def onJoin(self, details):

        # a simple procedure
        #
        def add2(x, y):
            print("add2() called with {} and {}".format(x, y))
            return x + y

        yield self.register(add2, 'com.example.add2')

        # a procedure returning a positional result
        #
        def split_name(fullname):
            print("split_name() called with '{}'".format(fullname))
            parts = fullname.split()
            return CallResult(*parts)

        yield self.register(split_name, 'com.example.split_name')

        # a procedure returning a keyword-base result
        #
        def add_complex(a, ai, b, bi):
            print("add_complex() called with {}".format((a, ai, b, bi)))
            return CallResult(c=a + b, ci=ai + bi)

        yield self.register(add_complex, 'com.example.add_complex')

        # raising standard exceptions
        #
        def sqrt(x):
            if x == 0:
                raise Exception("don't ask foolish questions;)")
            else:
                # this also will raise, if x < 0
                return math.sqrt(x)

        yield self.register(sqrt, 'com.example.sqrt')

        # raising WAMP application exceptions
        #
        def checkname(name):
            if name in ['foo', 'bar']:
                raise ApplicationError('com.example.error.reserved')

            if name.lower() != name and name.upper() != name:
                # forward positional arguments in exceptions
                raise ApplicationError('com.example.error.mixed_case', name.lower(), name, name.upper())

            if len(name) < 3 or len(name) > 10:
                # forward keyword arguments in exceptions
                raise ApplicationError('com.example.error.invalid_length', min=3, max=10)

        yield self.register(checkname, 'com.example.checkname')

        print("all procedures registered")
