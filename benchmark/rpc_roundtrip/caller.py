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
                res = yield self.call(u'{}.echo'.format(prefix), ts_req)
                ts_res = time()
                rtt = ts_res - ts_req
                rtts.append(rtt)
            batch_ended = time()
            batch_duration = float(batch_ended - batch_started)
            count = len(rtts)
            rtts = sorted(rtts)
            avg_rtt = round(1000. * batch_duration / float(count), 1)
            max_rtt = round(1000 * rtts[-1], 1)
            q50_rtt = round(1000 * rtts[count/2], 1)
            calls_per_sec = round(float(count) / batch_duration, 1)
            print("[{}] - {} calls | {} calls/sec; RTT (ms): avg {} | max {} | q50 {}".format(logname, count, calls_per_sec, avg_rtt, max_rtt, q50_rtt))

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

