from time import time
import argparse
import six

from zlmdb import time_ns, Database
from crossbar.common.processinfo import ProcessInfo
from twisted.internet.defer import inlineCallbacks, gatherResults
from autobahn.twisted.wamp import ApplicationSession
from autobahn.twisted.wamp import ApplicationRunner
from autobahn.util import utcnow
from autobahn.wamp.exception import TransportLost

from stats import Schema, ProcStatsRecord, WampStatsRecord


class AppSession(ApplicationSession):

    @inlineCallbacks
    def onJoin(self, details):
        self._db = Database(dbpath='../results')
        self._schema = Schema.attach(self._db)

        self._pinfo = ProcessInfo()
        self._logname = self.config.extra['logname']
        self._period = self.config.extra.get('period', 5.)
        self._running = True

        dl = []
        for i in range(8):
            d = self._loop(i)
            dl.append(d)

        d = gatherResults(dl)

        try:
            yield d
        except TransportLost:
            pass

    def onLeave(self, details):
        self._running = False

    @inlineCallbacks
    def _loop(self, index):
        prefix = self.config.extra['prefix']
        last = None

        while self._running:
            rtts = []

            batch_started_str = utcnow()
            batch_started = time()

            while (time() - batch_started) < self._period:
                ts_req = time_ns()
                res = yield self.call('{}.echo'.format(prefix), ts_req)
                ts_res = time_ns()
                assert res == ts_req
                rtt = ts_res - ts_req
                rtts.append(rtt)

            stats = self._pinfo.get_stats()

            if last:
                batch_duration = (stats['time'] - last['time']) / 10 ** 9
                ctx = round((stats['voluntary'] - last['voluntary']) / batch_duration, 0)

                self.log.info('{logname}: {cpu} cpu, {mem} mem, {ctx} ctx',
                              logname=self._logname,
                              cpu=round(stats['cpu_percent'], 1),
                              mem=round(stats['mem_percent'], 1),
                              ctx=ctx)

                rtts = sorted(rtts)

                sr = WampStatsRecord()
                sr.key = '{}#{}.{}'.format(batch_started_str, self._logname, index)
                sr.count = len(rtts)
                sr.calls_per_sec = int(round(sr.count / batch_duration, 0))

                # all times here are in microseconds:
                sr.avg_rtt = round(1000000. * batch_duration / float(sr.count), 1)
                sr.max_rtt = round(rtts[-1] / 1000, 1)
                sr.q50_rtt = round(rtts[int(sr.count / 2.)] / 1000, 1)
                sr.q99_rtt = round(rtts[int(-(sr.count / 100.))] / 1000, 1)
                sr.q995_rtt = round(rtts[int(-(sr.count / 995.))] / 1000, 1)

                with self._db.begin(write=True) as txn:
                    self._schema.wamp_stats[txn, sr.key] = sr

                print("{}: {} calls, {} calls/sec, RTT (us): q50 {}, avg {}, q99 {}, q995 {}, max {}".format(sr.key,
                                                                                                             sr.count,
                                                                                                             sr.calls_per_sec,
                                                                                                             sr.q50_rtt,
                                                                                                             sr.avg_rtt,
                                                                                                             sr.q99_rtt,
                                                                                                             sr.q995_rtt,
                                                                                                             sr.max_rtt))
            last = stats

if __name__ == '__main__':

    parser = argparse.ArgumentParser()

    parser.add_argument("--router", type=six.text_type, default=u"ws://10.1.1.11:9000", help='WAMP router URL.')
    parser.add_argument("--realm", type=six.text_type, default=u"realm1", help='WAMP router realm.')

    args = parser.parse_args()

    extra = {
        'prefix': 'com.example.websocket-json',
        'logname': 'WAMP-TCP-WebSocket-JSON'
    }

    runner = ApplicationRunner(url=args.router, realm=args.realm, extra=extra)
    runner.run(AppSession)

