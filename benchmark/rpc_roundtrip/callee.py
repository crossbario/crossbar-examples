from pprint import pformat
import txaio
from twisted.internet.defer import inlineCallbacks
from autobahn.twisted.wamp import ApplicationSession
from autobahn.wamp.types import RegisterOptions
from crossbar.common.processinfo import ProcessInfo
from autobahn.twisted.util import sleep
from crossbar._util import hl


class AppSession(ApplicationSession):

    log = txaio.make_logger()

    @inlineCallbacks
    def onJoin(self, details):

        self._prefix = self.config.extra['prefix']
        self._logname = self.config.extra['logname']
        self._count = 0

        self._pinfo = ProcessInfo()

        def echo(arg):
            self._count += 1
            return arg

        yield self.register(echo, '{}.echo'.format(self._prefix), options=RegisterOptions(invoke='roundrobin'))

        self.log.info('{} ready!'.format(self._logname))

        last = None
        while True:
            stats = self._pinfo.get_stats()
            if last:
                secs = (stats['time'] - last['time']) / 10**9
                calls_per_sec = int(round(self._count / secs, 0))
                ctx = round((stats['voluntary'] - last['voluntary']) / secs, 0)

                self.log.info('{logprefix}: {user} user, {system} system, {mem_percent} mem_percent, {ctx} ctx',
                              logprefix=hl('LOAD {}'.format(self._logname), color='cyan', bold=True),
                              user=stats['user'],
                              system=stats['system'],
                              mem_percent=round(stats['mem_percent'], 1),
                              ctx=ctx)
                self.log.info('{logprefix}: {calls} calls, {calls_per_sec} calls/second',
                              logprefix=hl('WAMP {}'.format(self._logname), color='cyan', bold=True),
                              calls=self._count,
                              calls_per_sec=hl(calls_per_sec, bold=True))

                self._count = 0

            last = stats
            yield sleep(10)
