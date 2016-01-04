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

from twisted.internet import reactor
from autobahn.twisted.wamp import ApplicationSession


TICKETS = {
   u'user1': u'123secret',
   u'user2': u'456secret'
}


class ClientSession(ApplicationSession):

   def onConnect(self):
      realm = self.config.realm
      authid = self.config.extra[u'authid']
      print("ClientSession connected. Joining realm <{}> under authid <{}>".format(realm if realm else 'not provided', authid))
      self.join(realm, [u'ticket'], authid)

   def onChallenge(self, challenge):
      print("ClientSession challenge received: {}".format(challenge))
      if challenge.method == u'ticket':
         authid = self.config.extra[u'authid']
         return TICKETS.get(self.config.extra[u'authid'], None)
      else:
         raise Exception("Invalid authmethod {}".format(challenge.method))

   def onJoin(self, details):
      print("ClientSession joined: {}".format(details))
      self.leave()

   def onLeave(self, details):
      print("ClientSession left: {}".format(details))
      self.disconnect()

   def onDisconnect(self):
      print("ClientSession disconnected")
      reactor.stop()


if __name__ == '__main__':

   import sys
   import argparse

   parser = argparse.ArgumentParser()
   parser.add_argument('--authid', dest='authid', type=unicode, default=u'user1', help='The authid to connect under (required)')
   parser.add_argument('--realm', dest='realm', type=unicode, default=None, help='The realm to join. If not provided, let the router auto-choose the realm (default).')
   parser.add_argument('--url', dest='url', type=unicode, default=u'ws://localhost:8080/ws', help='The router URL (default: ws://localhost:8080/ws).')
   options = parser.parse_args()

   from autobahn.twisted.wamp import ApplicationRunner

   if options.authid not in TICKETS:
      print("Given authid <{}> is not in my tickets database!".format(options.authid))
      sys.exit(1)

   extra = {
      u'authid': options.authid
   }
   print("Connecting to {}: realm={}, authid={}".format(options.url, options.realm, options.authid))

   runner = ApplicationRunner(url=options.url, realm=options.realm, extra=extra)
   runner.run(ClientSession)
