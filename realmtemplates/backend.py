from autobahn.twisted.wamp import ApplicationSession


class Backend(ApplicationSession):

   def onJoin(self, details):
      self.log.info("Backend connected: {details}", details=details)
