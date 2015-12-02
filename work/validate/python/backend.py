from autobahn.twisted.wamp import ApplicationSession

class MyComponent(ApplicationSession):

    def onJoin(self, details):
        print("connected")
