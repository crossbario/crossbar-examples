# -*- coding: utf-8 -*-

###############################################################################
##
##  Copyright (C) 2014 Michel Desmoulin
##
##  Licensed under the Apache License, Version 2.0 (the "License");
##  you may not use this file except in compliance with the License.
##  You may obtain a copy of the License at
##
##      http://www.apache.org/licenses/LICENSE-2.0
##
##  Unless required by applicable law or agreed to in writing, software
##  distributed under the License is distributed on an "AS IS" BASIS,
##  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
##  See the License for the specific language governing permissions and
##  limitations under the License.
##
###############################################################################


import socket
import uuid

from twisted.internet.defer import inlineCallbacks

from autobahn.twisted.util import sleep
from autobahn.twisted.wamp import ApplicationSession
from autobahn.wamp.exception import ApplicationError


class AppSession(ApplicationSession):

    @inlineCallbacks
    def onJoin(self, details):

        # We get our IP address on the local network.
        # It's a trick requiring an external IP to
        # be reachable, so you need an internet connection.
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        self._local_ip = s.getsockname()[0]
        s.close()

        def get_connection_data():
            connection_data = {}
            connection_data["ip"] = self._local_ip
            # We generate a UUID for the calling window
            # This is used to namespace the control to a particular player window
            connection_data["uuid"] = str(uuid.uuid4()).replace('-', '')
            return connection_data
        # We register the procedure yielding the connection data for remote calling
        reg_get_connection_data = yield self.register(get_connection_data, 'io.crossbar.demo.videocontroller.get_connection_data')
        print "procedure 'io.crossbar.demo.videocontroller.get_connection_data' registered"
