###############################################################################
##
##  Copyright (C) Tavendo GmbH and/or collaborators. All rights reserved.
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

import six
from twisted.internet import reactor
from autobahn.twisted.wamp import ApplicationSession


class ClientSession(ApplicationSession):

   def onJoin(self, details):
      self.log.info("ClientSession joined: {details}", details=details)
      self.log.info("\n\n*** Transport is using '{serializer}' serializer ***\n", serializer=self._transport._serializer.SERIALIZER_ID)
      self.leave()

   def onLeave(self, details):
      self.log.info("ClientSession left: {details}", details=details)
      self.disconnect()

   def onDisconnect(self):
      self.log.info("ClientSession disconnected")
      reactor.stop()


if __name__ == '__main__':

   import sys
   import argparse

   parser = argparse.ArgumentParser()
   parser.add_argument('--realm', dest='realm', type=six.text_type, default=u'realm1', help='The realm to join. If not provided, let the router auto-choose the realm (default).')
   parser.add_argument('--url', dest='url', type=six.text_type, default=u'ws://localhost:8080/ws', help='The router URL (default: ws://localhost:8080/ws).')
   options = parser.parse_args()

   from autobahn.twisted.wamp import ApplicationRunner

   extra = {
   }

   runner = ApplicationRunner(url=options.url, realm=options.realm, extra=extra)
   runner.run(ClientSession)
