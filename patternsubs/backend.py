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
from autobahn.wamp.types import SubscribeOptions
from autobahn.twisted.wamp import ApplicationSession


class MyComponent(ApplicationSession):

    @inlineCallbacks
    def onJoin(self, details):

        def handler1(msg, details = None):
            print("handler1: msg = '{0}', details = '{1}'".format(msg, details))

        yield self.subscribe(handler1, u"com.example.topic1", options=SubscribeOptions(details_arg="details"))

        def handler2(msg, details = None):
            print("handler2: msg = '{0}', details = '{1}'".format(msg, details))

        yield self.subscribe(handler2, u"com.example", options=SubscribeOptions(match=u"prefix", details_arg="details"))

        def handler3(msg, details = None):
            print("handler3: msg = '{0}', details = '{1}'".format(msg, details))

        yield self.subscribe(handler3, u"com..topic1", options=SubscribeOptions(match=u"wildcard", details_arg="details"))

        print("MyComponent: all event handlers subscribed!")
