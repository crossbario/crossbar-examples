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

import os

from twisted.internet import reactor
from twisted.internet.defer import inlineCallbacks, Deferred, returnValue
from twisted.internet.protocol import Factory
from twisted.internet.endpoints import UNIXClientEndpoint
from twisted.conch.ssh.agent import SSHAgentClient

from autobahn.twisted.wamp import ApplicationSession
from autobahn.wamp import cryptosign

from autobahn.wamp.cryptosign import SigningKey


from binascii import a2b_hex, b2a_hex

import struct

def sign_via_ssh_agent(reactor, pubkey, challenge):
    if "SSH_AUTH_SOCK" not in os.environ:
        raise Exception("no ssh-agent is running!")

    print("Using public key {}".format(b2a_hex(pubkey)))

    factory = Factory()
    factory.protocol = SSHAgentClient
    endpoint = UNIXClientEndpoint(reactor, os.environ["SSH_AUTH_SOCK"])
    d = endpoint.connect(factory)

    @inlineCallbacks
    def on_connect(agent):
        # we are now connected to the locally running ssh-agent
        # that agent might be the openssh-agent, or eg on Ubuntu 14.04 by
        # default the gnome-keyring / ssh-askpass-gnome application
        print("connected to ssh-agent!")

        blob = cryptosign.pack(['ssh-ed25519', pubkey])

        # now ask the agent
        signature_blob = yield agent.signData(blob, challenge)
        algo, signature = cryptosign.unpack(signature_blob)
        print(algo)
        print(b2a_hex(signature))

        agent.transport.loseConnection()

        returnValue(signature)

    return d.addCallback(on_connect)


class ClientSession(ApplicationSession):

    @inlineCallbacks
    def onConnect(self):
        print("onConnect()")
        self._key = yield SigningKey.from_ssh_agent(self.config.extra[u'pubkey'])
        self.join(self.config.realm, authmethods=[u'cryptosign'], authid=self.config.extra[u'authid'])

    @inlineCallbacks
    def onChallenge(self, challenge):
        print("onChallenge(challenge={})".format(challenge))
        sig = yield sign_via_ssh_agent(reactor, a2b_hex(self._key.public_key()), a2b_hex(challenge.extra[u'challenge']))
        sig = b2a_hex(sig)
        returnValue(sig + challenge.extra[u'challenge'])

    def onJoin(self, details):
        print("onJoin(details={})".format(details))
        print("\nHooray! We've been successfully authenticated with WAMP-cryptosign using Ed25519!\n")
        self.leave()

    def onLeave(self, details):
        print("onLeave(details={})".format(details))
        self.disconnect()

    def onDisconnect(self):
        print("onDisconnect()")
        reactor.stop()


if __name__ == '__main__':

    import six
    import sys
    import argparse
    from autobahn.twisted.wamp import ApplicationRunner

    # parse command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--authid', dest='authid', type=six.text_type, default=None, help='The authid to connect under. If not provided, let the router auto-choose the authid.')
    parser.add_argument('--realm', dest='realm', type=six.text_type, default=None, help='The realm to join. If not provided, let the router auto-choose the realm.')
    parser.add_argument('--pubkey', dest='pubkey', type=six.text_type, help='Filename of SSH Ed25519 public key.')
    parser.add_argument('--routerkey', dest='routerkey', type=six.text_type, default=None, help='The public router key to verify the remote router against. A 32 bytes file containing the raw Ed25519 public key.')
    parser.add_argument('--url', dest='url', type=six.text_type, default=u'ws://localhost:8080/ws', help='The router URL (default: ws://localhost:8080/ws).')
    parser.add_argument('--agent', dest='agent', type=six.text_type, default=None, help='Path to Unix domain socket of SSH agent to use.')
    parser.add_argument('--trace', dest='trace', action='store_true', default=False, help='Trace traffic: log WAMP messages sent and received')
    options = parser.parse_args()

    with open(options.pubkey) as f:
        pubkey = f.read()

    extra = {
        u'authid': options.authid,
        u'pubkey': pubkey
    }
    print("Connecting to {}: realm={}, authid={}".format(options.url, options.realm, options.authid))

    # connect to router and run ClientSession
    runner = ApplicationRunner(url=options.url, realm=options.realm, extra=extra, debug_wamp=options.trace)
    runner.run(ClientSession)
