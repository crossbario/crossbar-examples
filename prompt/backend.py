from twisted.internet.defer import inlineCallbacks
from twisted.internet.task import LoopingCall
from autobahn.twisted.wamp import ApplicationSession

def add2(a, b):
    print('add2 called: {} {}'.format(a, b))
    return a + b


class Backend(ApplicationSession):

    @inlineCallbacks
    def onJoin(self, details):
        c = LoopingCall(self.publish, u'com.example.tick')
        c.start(1)

        yield self.register(add2, u'com.example.add2')
        self.log.info('backend ready!')
