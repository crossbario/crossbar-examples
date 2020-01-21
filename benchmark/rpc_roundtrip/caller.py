import numpy as np

from time import time
import argparse
import six

from zlmdb import time_ns, Database
from crossbar.common.processinfo import ProcessInfo
from twisted.internet.defer import inlineCallbacks, gatherResults
from twisted.internet.task import LoopingCall

from autobahn.twisted.wamp import ApplicationSession
from autobahn.twisted.wamp import ApplicationRunner
from autobahn.wamp.exception import TransportLost
import uuid
from crossbar._util import hl

from stats import Schema, ProcStatsRecord, WampStatsRecord


class AppSession(ApplicationSession):

    @inlineCallbacks
    def onJoin(self, details):
        self._db = Database(dbpath='../results')
        self._schema = Schema.attach(self._db)

        self._pinfo = ProcessInfo()
        self._logname = self.config.extra['logname']
        self._period = self.config.extra.get('period', 10.)
        self._running = True

        batch_id = uuid.uuid4()

        self._last_stats = None
        self._stats_loop = LoopingCall(self._stats, batch_id)
        self._stats_loop.start(self._period)

        dl = []
        for i in range(8):
            d = self._loop(batch_id, i)
            dl.append(d)
        d = gatherResults(dl)

        try:
            yield d
        except TransportLost:
            pass

    def onLeave(self, details):
        self._running = False
        self._stats_loop.stop()

    def _stats(self, batch_id):
        stats = self._pinfo.get_stats()

        if self._last_stats:
            batch_duration = (stats['time'] - self._last_stats['time']) / 10 ** 9
            ctx = round((stats['voluntary'] - self._last_stats['voluntary']) / batch_duration, 0)
            self.log.info('{logprefix}: {user} user, {system} system, {mem_percent} mem_percent, {ctx} ctx',
                          logprefix=hl('LOAD {}.*'.format(self._logname), color='magenta', bold=True),
                          logname=self._logname,
                          user=stats['user'],
                          system=stats['system'],
                          mem_percent=round(stats['mem_percent'], 1),
                          ctx=ctx)

        self._last_stats = stats

    @inlineCallbacks
    def _loop(self, batch_id, index):
        prefix = self.config.extra['prefix']

        while self._running:
            rtts = []

            self.log.debug('{logprefix} is starting new period ..',
                           logprefix=hl('     {}.{}'.format(self._logname, index), color='magenta', bold=True),)

            batch_started = time_ns()

            while float(time_ns() - batch_started) / 10**9 < self._period:
                ts_req = time_ns()
                res = yield self.call('{}.echo'.format(prefix), ts_req)
                ts_res = time_ns()
                assert res == ts_req
                rtt = ts_res - ts_req
                rtts.append(rtt)

            batch_duration = float(time_ns() - batch_started) / 10**9

            rtts = sorted(rtts)

            sr = WampStatsRecord()
            sr.worker = int(self._logname.split('.')[1])
            sr.loop = index
            sr.count = len(rtts)
            sr.calls_per_sec = int(round(sr.count / batch_duration, 0))

            # all times here are in microseconds:
            sr.avg_rtt = int(round(1000000. * batch_duration / float(sr.count), 0))
            sr.max_rtt = int(round(rtts[-1] / 1000, 0))
            sr.q50_rtt = int(round(rtts[int(sr.count / 2.)] / 1000, 0))
            sr.q99_rtt = int(round(rtts[int(-(sr.count / 100.))] / 1000, 0))
            sr.q995_rtt = int(round(rtts[int(-(sr.count / 995.))] / 1000, 0))

            try:
                with self._db.begin(write=True) as txn:
                    self._schema.wamp_stats[txn, (batch_id, np.datetime64(batch_started, 'ns'))] = sr
            except:
                self.log.failure()
                return self.leave()

            self.log.info("{logprefix}: {count} calls, {calls_per_sec}, round-trip time (microseconds): q50 {q50_rtt}, avg {avg_rtt}, {q99_rtt}, q995 {q995_rtt}, max {max_rtt}".format(
                logprefix=hl('WAMP {}.{}'.format(self._logname, index), color='magenta', bold=True),
                count=sr.count,
                calls_per_sec=hl('{} calls/second'.format(sr.calls_per_sec), bold=True),
                q50_rtt=sr.q50_rtt,
                avg_rtt=sr.avg_rtt,
                q99_rtt=hl('q99 {}'.format(sr.q99_rtt), bold=True),
                q995_rtt=sr.q995_rtt,
                max_rtt=sr.max_rtt))


if __name__ == '__main__':

    parser = argparse.ArgumentParser()

    parser.add_argument("--router", type=str, default="ws://10.1.1.11:9000", help='WAMP router URL.')
    parser.add_argument("--realm", type=str, default="realm1", help='WAMP router realm.')

    args = parser.parse_args()

    extra = {
        'prefix': 'com.example.websocket-json',
        'logname': 'WAMP-TCP-WebSocket-JSON'
    }

    runner = ApplicationRunner(url=args.router, realm=args.realm, extra=extra)
    runner.run(AppSession)

