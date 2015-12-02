from twisted.logger import Logger
from twisted.internet.defer import inlineCallbacks
from autobahn.twisted.wamp import ApplicationSession
from autobahn.twisted.util import sleep

class MySession(ApplicationSession):

    log = Logger()

    def __init__(self, config):
        self.log.info("MySession.__init__()")
        ApplicationSession.__init__(self, config)

    @inlineCallbacks
    def onJoin(self, details):
        self.log.info("MySession.onJoin()")
        self.log.info("Sleeping a couple fo secs and then shutting down ..")
        yield sleep(2)
        self.leave()

    def onLeave(self, details):
        self.log.info("Session ended: {details}", details=details)
        self.disconnect()
