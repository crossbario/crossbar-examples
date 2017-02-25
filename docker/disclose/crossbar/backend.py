from autobahn.twisted.wamp import ApplicationSession


class Backend(ApplicationSession):

    def onJoin(self, details):
        print('connected!')

