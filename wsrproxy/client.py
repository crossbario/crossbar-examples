import argparse

from twisted.internet import reactor
from twisted.internet.endpoints import clientFromString

import txaio

from autobahn.twisted.websocket import WebSocketClientProtocol, \
    WebSocketClientFactory


class MyClientProtocol(WebSocketClientProtocol):

    def onConnect(self, response):
        print("Server connected: {0}".format(response.peer))
        self.counter = 0

    def onOpen(self):
        print("WebSocket connection open.")

        def hello():
            self.sendMessage("Hello, world!".encode('utf8'))
            self.sendMessage(b"\x00\x01\x03\x04", isBinary=True)
            self.counter += 1
            if self.counter > 2:
                self.sendClose()
            else:
                self.factory.reactor.callLater(1, hello)

        # start sending messages every second ..
        hello()

    def onMessage(self, payload, isBinary):
        if isBinary:
            print("Binary message received: {0} bytes".format(len(payload)))
        else:
            print("Text message received: {0}".format(payload.decode('utf8')))

    def onClose(self, wasClean, code, reason):
        print("WebSocket connection closed: {0}".format(reason))
        reactor.stop()


if __name__ == '__main__':

    parser = argparse.ArgumentParser()

    parser.add_argument("-d", "--debug", action="store_true",
                        help="Enable debug output.")

    parser.add_argument("--endpoint", default="tcp:127.0.0.1:8080",
                        help='WebSocket client Twisted endpoint descriptor, e.g. "tcp:127.0.0.1:8080" or "unix:/tmp/mywebsocket".')

    parser.add_argument("--url", default="ws://localhost:8080/ws",
                        help='WebSocket URL (must suit the endpoint), e.g. ws://localhost:8080/ws.')

    args = parser.parse_args()

    if args.debug:
        txaio.start_logging(level='debug')
    else:
        txaio.start_logging(level='info')

    factory = WebSocketClientFactory(args.url, reactor=reactor)
    factory.protocol = MyClientProtocol

    client = clientFromString(reactor, args.endpoint)
    client.connect(factory)

    reactor.run()
