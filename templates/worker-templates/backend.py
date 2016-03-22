from autobahn.twisted.wamp import ApplicationSession


class Backend(ApplicationSession):

   def onJoin(self, details):
      self.log.info("Backend connected: realm '{realm}', authid '{authid}'", realm=details.realm, authid=details.authid)
