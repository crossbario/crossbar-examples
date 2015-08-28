from twisted.logger import Logger
from autobahn.twisted.wamp import ApplicationSession

class MySession(ApplicationSession):

    log = Logger()

    def __init__(self, config):
        self.log.info("MySession.__init__()")
        ApplicationSession.__init__(self, config)

    def onJoin(self, details):
        self.log.info("MySession.onJoin()")
        self.leave()

    def onLeave(self, details):
        self.log.info("Session ended: {details}", details=details)
        self.disconnect()
