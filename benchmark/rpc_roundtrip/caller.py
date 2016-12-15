from time import time
import argparse
import six
from twisted.internet.defer import inlineCallbacks
from autobahn.twisted.wamp import ApplicationSession
from autobahn.twisted.wamp import ApplicationRunner
from autobahn.twisted.util import sleep


class AppSession(ApplicationSession):

    @inlineCallbacks
    def onJoin(self, details):

        prefix = self.config.extra[u'prefix']
        logname = self.config.extra[u'logname']
        period = self.config.extra.get(u'period', 2.)

        while True:
            rtts = []
            batch_started = time()
            while (time() - batch_started) < period:
                ts_req = time()
                res = yield self.call(u'{}.echo'.format(prefix), counter)
                ts_res = time()
                rtt = ts_res - ts_req
                rtts.append(rtt)
            batch_ended = time()
            count = len(rtts)
            avg_rtt = 1000. * float(batch_ended - batch_started) / float(count)
            print("[{}] - average round-trip time (ms): {}".format(logname, avg_rtt))

if __name__ == '__main__':

    parser = argparse.ArgumentParser()

    parser.add_argument("--router", type=six.text_type, default=u"ws://10.1.1.11:9000", help='WAMP router URL.')
    parser.add_argument("--realm", type=six.text_type, default=u"realm1", help='WAMP router realm.')

    args = parser.parse_args()

    extra = {
        u'prefix': u'com.example.websocket-json',
        u'logname': u'WAMP-TCP-WebSocket-JSON'
    }

    runner = ApplicationRunner(url=args.router, realm=args.realm, extra=extra)
    runner.run(AppSession)

