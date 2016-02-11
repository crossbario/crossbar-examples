from time import time
from twisted.internet.defer import inlineCallbacks
from autobahn.twisted.wamp import ApplicationSession
from autobahn.twisted.util import sleep


class AppSession(ApplicationSession):

    @inlineCallbacks
    def onJoin(self, details):

        prefix = self.config.extra[u'prefix']
        logname = self.config.extra[u'logname']

        counter = 0
        batch_size = 1000
        ts_start = time()
        while True:
            counter += 1
            res = yield self.call(u'{}.echo'.format(prefix), counter)
            if counter % batch_size == 0:
                ts_end = time()
                avg_rtt = 1000. * float(ts_end - ts_start) / float(batch_size)
                print("[{}] - average round-trip time (ms): {}".format(logname, avg_rtt))
                ts_start = ts_end
