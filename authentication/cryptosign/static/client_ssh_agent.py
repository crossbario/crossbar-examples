###############################################################################
##
# Copyright (C) Tavendo GmbH and/or collaborators. All rights reserved.
##
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
##
# 1. Redistributions of source code must retain the above copyright notice,
# this list of conditions and the following disclaimer.
##
# 2. Redistributions in binary form must reproduce the above copyright notice,
# this list of conditions and the following disclaimer in the documentation
# and/or other materials provided with the distribution.
##
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
##
###############################################################################

import os

from twisted.internet import reactor
from twisted.internet.defer import inlineCallbacks

from autobahn import util
from autobahn.twisted.wamp import ApplicationSession
from autobahn.twisted.cryptosign import SSHAgentCryptosignKey


class ClientSession(ApplicationSession):
    """
    A WAMP client component authenticating using WAMP-cryptosign using
    a private (Ed25519) key held in SSH agent.
    """
    # when running over TLS, require TLS channel binding
    # CHANNEL_BINDING = 'tls-unique'
    CHANNEL_BINDING = None

    @inlineCallbacks
    def onConnect(self):
        print("onConnect()")

        print('Using public key from {}'.format(self.config.extra['pubkey']))

        # create a proxy signing key with the private key being held in SSH agent
        self._key = yield SSHAgentCryptosignKey.new(self.config.extra['pubkey'])

        print('Public key: {}'.format(self._key.public_key()))

        # authentication extra information for wamp-cryptosign
        extra = {
            # forward the client pubkey: this allows us to omit authid as
            # the router can identify us with the pubkey already
            'pubkey': self._key.public_key(),

            # when running over TLS, require TLS channel binding
            'channel_binding': ClientSession.CHANNEL_BINDING,
        }

        # join and authenticate using WAMP-cryptosign
        self.join(self.config.realm,
                  authmethods=['cryptosign'],
                  authid=self.config.extra['authid'],
                  authextra=extra)

    def onChallenge(self, challenge):
        print("onChallenge(challenge={})".format(challenge))

        signed_challenge = self._key.sign_challenge(challenge,
                                                    channel_id=self.transport.transport_details.channel_id.get(ClientSession.CHANNEL_BINDING, None),
                                                    channel_id_type=ClientSession.CHANNEL_BINDING)

        # send back the signed challenge for verification
        return signed_challenge

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

    import argparse
    from autobahn.twisted.wamp import ApplicationRunner

    # parse command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--authid', dest='authid', type=str, default=None,
                        help='The authid to connect under. If not provided, let the router auto-choose the authid (based on client public key).')
    parser.add_argument('--realm', dest='realm', type=str, default=None,
                        help='The realm to join. If not provided, let the router auto-choose the realm.')
    parser.add_argument('--pubkey', dest='pubkey', type=str, default=None,
                        help='Filename of the client SSH Ed25519 public key.')
    parser.add_argument('--trustroot', dest='trustroot', type=str, default=None,
                        help='Filename of the router SSH Ed25519 public key (for server verification).')
    parser.add_argument('--url', dest='url', type=str, default='ws://localhost:8080/ws',
                        help='The router URL (default: ws://localhost:8080/ws).')
    parser.add_argument('--agent', dest='agent', type=str, default=None,
                        help='Path to Unix domain socket of SSH agent to use.')
    parser.add_argument('--trace', dest='trace', action='store_true',
                        default=False, help='Trace traffic: log WAMP messages sent and received')
    options = parser.parse_args()

    print("Connecting to {}: realm={}, authid={}, pubkey={}, trustroot={}".format(
        options.url, options.realm, options.authid, options.pubkey, options.trustroot))

    if options.pubkey is None:
        options.pubkey = os.path.expanduser('~/.ssh/id_ed25519.pub')

    # load client public key
    with open(options.pubkey, 'r') as f:
        pubkey = f.read()
        if type(pubkey) == bytes:
            pubkey = pubkey.decode('ascii')

    # load router public key (optional, if avail., router will be authenticated too)
    trustroot = None
    if options.trustroot:
        with open(options.trustroot, 'r') as f:
            trustroot = f.read()
            if type(trustroot) == bytes:
                trustroot = trustroot.decode('ascii')

    # forward stuff to our session
    extra = {
        'authid': options.authid,
        'pubkey': pubkey,
        'trustroot': trustroot
    }

    runner = ApplicationRunner(
        url=options.url, realm=options.realm, extra=extra)
    runner.run(ClientSession)
