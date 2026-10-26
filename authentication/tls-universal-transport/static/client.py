"""A WAMP client for the universal transport: WebSocket or RawSocket, over TLS,
authenticated with WAMP-Cryptosign.

    python client.py --transport websocket --key ../../cryptosign/tls/.keys/client01.key
    python client.py --transport rawsocket --key ../../cryptosign/tls/.keys/client01.key

It trusts exactly the router's certificate (--trust, default .crossbar/server.crt),
joins the realm, prints the session details and leaves. Without --key it offers only
anonymous authentication, which the router refuses.
"""

import argparse

from autobahn.twisted.wamp import ApplicationRunner, ApplicationSession
from autobahn.wamp import cryptosign
from twisted.internet import ssl

parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
parser.add_argument("--transport", choices=["websocket", "rawsocket"], default="websocket")
parser.add_argument("--host", default="localhost", help="the router's host (default: localhost)")
parser.add_argument("--port", type=int, default=8080)
parser.add_argument("--servername", default="localhost", help="the name the certificate is checked for")
parser.add_argument("--trust", default=".crossbar/server.crt", help="the certificate to trust")
parser.add_argument("--key", default=None, help="a Cryptosign private key file (none: anonymous)")
parser.add_argument("--realm", default="devices")
args = parser.parse_args()


class Client(ApplicationSession):

    def onConnect(self):
        if args.key is None:
            self.join(args.realm, authmethods=["anonymous"])
            return
        self._key = cryptosign.CryptosignKey.from_file(args.key)
        self.join(args.realm, authmethods=["cryptosign"], authextra={"pubkey": self._key.public_key()})

    def onChallenge(self, challenge):
        return self._key.sign_challenge(challenge)

    def onJoin(self, details):
        print(f"joined: realm={details.realm} authid={details.authid} authrole={details.authrole}"
              f" authmethod={details.authmethod} transport={args.transport}", flush=True)
        self.leave()

    def onLeave(self, details):
        print(f"left: reason={details.reason} message={details.message}", flush=True)
        self.disconnect()

    def onDisconnect(self):
        from twisted.internet import reactor
        if reactor.running:
            reactor.stop()


if __name__ == "__main__":
    with open(args.trust) as f:
        trust = ssl.Certificate.loadPEM(f.read())
    tls = ssl.optionsForClientTLS(args.servername, trustRoot=trust)
    scheme, path = ("wss", "/ws") if args.transport == "websocket" else ("rss", "")
    url = f"{scheme}://{args.host}:{args.port}{path}"
    ApplicationRunner(url, args.realm, ssl=tls).run(Client)
