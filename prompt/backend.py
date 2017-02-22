from twisted.internet.defer import inlineCallbacks
from twisted.internet.task import LoopingCall
from autobahn.twisted.wamp import ApplicationSession

def add2(a, b):
    print('add2 called: {} {}'.format(a, b))
    return a + b

def validate_int(num):
    print('validate_int called: {}'.format(num))
    try:
        int(num)
        return True
    except ValueError:
        return False

class Backend(ApplicationSession):

    @inlineCallbacks
    def onJoin(self, details):
        c = LoopingCall(self.publish, u'com.example.tick')
        c.start(1)

        yield self.register(add2, u'com.example.add2')
        yield self.register(validate_int, u'com.example.validate_int')

        self.log.info('backend ready!')
