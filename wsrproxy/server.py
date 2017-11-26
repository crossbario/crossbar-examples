import argparse

from twisted.internet import reactor
from twisted.internet.endpoints import serverFromString

import txaio

from autobahn.twisted.websocket import WebSocketServerProtocol, \
    WebSocketServerFactory


class MyServerProtocol(WebSocketServerProtocol):

    def onConnect(self, request):
        print("Client connecting: {0}".format(request.peer))

    def onOpen(self):
        print("WebSocket connection open.")

    def onMessage(self, payload, isBinary):
        if isBinary:
            print("Binary message received: {0} bytes".format(len(payload)))
        else:
            print("Text message received: {0}".format(payload.decode('utf8')))

        # echo back message verbatim
        self.sendMessage(payload, isBinary)

    def onClose(self, wasClean, code, reason):
        print("WebSocket connection closed: {0}".format(reason))


if __name__ == '__main__':

    parser = argparse.ArgumentParser()

    parser.add_argument("-d", "--debug", action="store_true",
                        help="Enable debug output.")

    parser.add_argument("--endpoint", default="tcp:8080",
                        help='WebSocket server Twisted endpoint descriptor, e.g. "tcp:127.0.0.1:8080" or "unix:/tmp/mywebsocket".')

    parser.add_argument("--url", default=u"ws://localhost:8080/ws",
                        help='WebSocket URL (must suit the endpoint), e.g. ws://localhost:8080/ws.')

    args = parser.parse_args()

    if args.debug:
        txaio.start_logging(level='debug')
    else:
        txaio.start_logging(level='info')

    factory = WebSocketServerFactory(args.url, reactor=reactor)
    factory.protocol = MyServerProtocol

    server = serverFromString(reactor, args.endpoint)
    server.listen(factory)

    reactor.run()
