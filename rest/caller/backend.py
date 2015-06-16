###############################################################################
##
##  Copyright (C) 2015, Tavendo GmbH and/or collaborators. All rights reserved.
##
##  Redistribution and use in source and binary forms, with or without
##  modification, are permitted provided that the following conditions are met:
##
##  1. Redistributions of source code must retain the above copyright notice,
##     this list of conditions and the following disclaimer.
##
##  2. Redistributions in binary form must reproduce the above copyright notice,
##     this list of conditions and the following disclaimer in the documentation
##     and/or other materials provided with the distribution.
##
##  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
##  AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
##  IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
##  ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
##  LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
##  CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
##  SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
##  INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
##  CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
##  ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
##  POSSIBILITY OF SUCH DAMAGE.
##
###############################################################################

import math

from twisted.internet.defer import inlineCallbacks

from autobahn.twisted.util import sleep
from autobahn.twisted.wamp import ApplicationSession
from autobahn.wamp.exception import ApplicationError
from autobahn.wamp.types import CallResult


class AppSession(ApplicationSession):

    @inlineCallbacks
    def onJoin(self, details):

        # a simple procedure
        #
        def add2(x, y):
            print("add2() called with {} and {}".format(x, y))
            return x + y

        yield self.register(add2, u'com.example.add2')

        # a procedure returning a positional result
        #
        def split_name(fullname):
            print("split_name() called with '{}'".format(fullname))
            parts = fullname.split()
            return CallResult(*parts)

        yield self.register(split_name, u'com.example.split_name')

        # a procedure returning a keyword-base result
        #
        def add_complex(a, ai, b, bi):
            print("add_complex() called with {}".format((a, ai, b, bi)))
            return CallResult(c=a + b, ci=ai + bi)

        yield self.register(add_complex, u'com.example.add_complex')

        # raising standard exceptions
        #
        def sqrt(x):
            if x == 0:
                raise Exception("don't ask foolish questions;)")
            else:
                # this also will raise, if x < 0
                return math.sqrt(x)

        yield self.register(sqrt, u'com.example.sqrt')

        # raising WAMP application exceptions
        #
        def checkname(name):
            if name in ['foo', 'bar']:
                raise ApplicationError(u'com.example.error.reserved')

            if name.lower() != name and name.upper() != name:
                # forward positional arguments in exceptions
                raise ApplicationError(u'com.example.error.mixed_case', name.lower(), name, name.upper())

            if len(name) < 3 or len(name) > 10:
                # forward keyword arguments in exceptions
                raise ApplicationError(u'com.example.error.invalid_length', min=3, max=10)

        yield self.register(checkname, u'com.example.checkname')

        print("all procedures registered")
