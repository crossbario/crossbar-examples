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

import os

from twisted.internet.defer import inlineCallbacks

from autobahn import wamp
from autobahn.wamp.types import RegisterOptions
from autobahn.twisted.wamp import ApplicationSession


class MyComponent(ApplicationSession):

    @inlineCallbacks
    def onJoin(self, details):

        def endpoint1(msg, details = None):
            print("endpoint1: msg = '{0}', details = '{1}'".format(msg, details))
            return u'endpoint1'

        yield self.register(endpoint1, u"com.example.procedure1", options=RegisterOptions(details_arg="details"))

        def endpoint2(msg, details = None):
            print("endpoint2: msg = '{0}', details = '{1}'".format(msg, details))
            return u'endpoint2'

        yield self.register(endpoint2, u"com.example", options=RegisterOptions(match=u"prefix", details_arg="details"))

        def endpoint2b(msg, details = None):
            print("endpoint2b: msg = '{0}', details = '{1}'".format(msg, details))
            return u'endpoint2b'

        yield self.register(endpoint2b, u"com.example.", options=RegisterOptions(match=u"prefix", details_arg="details"))

        def endpoint3(msg, details = None):
            print("endpoint3: msg = '{0}', details = '{1}'".format(msg, details))
            return u'endpoint3'

        yield self.register(endpoint3, u"com..procedure1", options=RegisterOptions(match=u"wildcard", details_arg="details"))

        print("MyComponent: all procedure endpoints registered!")
