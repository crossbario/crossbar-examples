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


class ClientSession(ApplicationSession):

    def onConnect(self):
        print("Client session connected.")

        # join the realm under the specified authid, and perform WAMP-ticket authentication
        self.join(self.config.realm, [u"ticket"], self.config.extra[u'authid'])

    def onChallenge(self, challenge):
        if challenge.method == u"ticket":
            print("WAMP-Ticket challenge received: {}".format(challenge))
            return self.config.extra[u'ticket']
        else:
            raise Exception("Invalid authmethod {}".format(challenge.method))

    def onJoin(self, details):
        print("Client session joined: {}".format(details))
        print("\nHooray! We've been successfully authenticated with WAMP-Ticket using TOTP!\n")
        self.leave()

    def onLeave(self, details):
        print("Client session left: {}".format(details))
        self.disconnect()

    def onDisconnect(self):
        print("Client session disconnected.")
        reactor.stop()


if __name__ == '__main__':

    import six
    import argparse
    from autobahn.twisted.wamp import ApplicationRunner

    parser = argparse.ArgumentParser()
    parser.add_argument('--url', dest='url', type=six.text_type, default=u'ws://localhost:8080/ws', help='The router URL (default: ws://localhost:8080/ws).')
    parser.add_argument('--realm', dest='realm', type=six.text_type, default=u'realm1', help='The realm to join. If not provided, let the router auto-choose the realm.')
    parser.add_argument('--authid', dest='authid', type=six.text_type, default=u'tobias1', help='The authid to connect under. If not provided, let the router auto-choose the authid (based on client public key).')
    parser.add_argument('--ticket', dest='ticket', type=six.text_type, help='The authid to connect under. If not provided, let the router auto-choose the authid (based on client public key).')
    options = parser.parse_args()

    ticket = options.ticket
    if not ticket:
        ticket = six.moves.input('Enter current TOTP value for authid "{}" (e.g. "522955"): '.format(options.authid))

    extra = {
        u'authid': options.authid,
        u'ticket': ticket
    }

    runner = ApplicationRunner(url=options.url, realm=options.realm, extra=extra)
    runner.run(ClientSession)
