import os
import six

from twisted.internet.defer import inlineCallbacks

from autobahn import util
from autobahn.twisted.wamp import ApplicationSession
from autobahn.wamp.exception import ApplicationError


class Backend(ApplicationSession):

    @inlineCallbacks
    def onJoin(self, details):

        self.log.info("BACKEND joined: {details}", details=details)

        def add2(x, y):
            self.log.info("add2({x}, {y}) called", x=x, y=y)
            return x + y

        yield self.register(add2, u'com.example.add2')

        def rand(n=8):
            self.log.info("rand(n={n}) called", n=n)
            return os.urandom(n)

        yield self.register(rand, u'com.example.rand')

        def blen(binary):
            if type(binary) != six.binary_type:
                raise ApplicationError(u'com.example.error.invalid_type', u'expected binary, got {}'.format(type(binary)))
            return len(binary)

        yield self.register(blen, u'com.example.blen')

        def xor(bin1, bin2):
            return util.xor(bin1, bin2)

        yield self.register(xor, u'com.example.xor')

        self.log.info("BACKEND READY!")
