from pprint import pformat
import txaio
from twisted.internet.defer import inlineCallbacks
from autobahn.twisted.wamp import ApplicationSession
from autobahn.wamp.types import RegisterOptions
from crossbar.common.processinfo import ProcessInfo
from autobahn.twisted.util import sleep

class AppSession(ApplicationSession):

    log = txaio.make_logger()

    @inlineCallbacks
    def onJoin(self, details):

        self._prefix = self.config.extra['prefix']
        self._logname = self.config.extra['logname']

        self._pinfo = ProcessInfo()

        def echo(arg):
            return arg

        yield self.register(echo, '{}.echo'.format(self._prefix), options=RegisterOptions(invoke='roundrobin'))

        self.log.info('{} ready!'.format(self._logname))

        last = None
        while True:
            stats = self._pinfo.get_stats()
            if last:
                secs = (stats['time'] - last['time']) / 10**9
                ctx = round((stats['voluntary'] - last['voluntary']) / secs, 0)
                self.log.info('{logname}: {cpu} cpu, {mem} mem, {ctx} ctx',
                              logname=self._logname,
                              cpu=round(stats['cpu_percent'], 1),
                              mem=round(stats['mem_percent'], 1),
                              ctx=ctx)
            last = stats
            yield sleep(5)
