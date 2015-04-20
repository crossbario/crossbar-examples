# Copyright (C) Tavendo GmbH. Open-source licensed under the
# MIT License (http://opensource.org/licenses/MIT)

import sys
import argparse
import math
import random

from twisted.python import log
from twisted.internet.defer import inlineCallbacks
from twisted.internet.threads import deferToThread
from twisted.internet.task import LoopingCall

from autobahn.twisted.wamp import ApplicationSession
from autobahn.twisted.wamp import ApplicationRunner


class PiMonitor(ApplicationSession):

    @inlineCallbacks
    def onJoin(self, details):
        log.msg("PiMonitor connected")

        extra = self.config.extra

        self._id = extra['id']

        self._tick = 0
        self._cpu_temp_celsius = None

        def scanTemperature():
            self._cpu_temp_celsius = float(open("/sys/class/thermal/thermal_zone0/temp").read()) / 1000.
            self.publish(u'com.example.device.{}.monitor.on_temperature'.format(self._id), self._tick, self._cpu_temp_celsius)
            self._tick += 1

        scan = LoopingCall(scanTemperature)
        scan.start(1)

        for proc in [self.get_temperature, self.impose_stress]:
            uri = u'com.example.device.{}.monitor.{}'.format(self._id, proc.__name__)
            yield self.register(proc, uri)
            log.msg("Registered {}".format(uri))

        log.msg("PiMonitor ready.")

    def get_temperature(self):
        return self._cpu_temp_celsius


    def impose_stress(self, n):
        def _stress():
            val = 0
            for _ in range(0, n):
                val += math.sin(random.random())
            return val / float(n)

        return deferToThread(_stress)


def get_serial():
    """
    Get the Pi's serial number.
    """
    try:
        with open('/proc/cpuinfo') as f:
            for line in f.read().splitlines():
               if line.startswith('Serial'):
                   return line.split(':')[1].strip()[8:]
    except:
        pass
    return "00000000"


if __name__ == '__main__':

    # parse command line arguments
    #
    parser = argparse.ArgumentParser()

    parser.add_argument("-d", "--debug", action="store_true",
                        help="Enable debug output.")

    parser.add_argument("--router", type=unicode, required=True,
                        help='URL of WAMP router to connect to.')

    parser.add_argument("--realm", type=unicode, default=u"realm1",
                        help='The WAMP realm to join on the router.')

    parser.add_argument("--id", type=unicode, default=None,
                        help='Client ID.')

    args = parser.parse_args()

    log.startLogging(sys.stdout)

    if args.id is None:
        args.id = get_serial()

    log.msg("Flite2Wamp bridge starting with ID {} ...".format(args.id))

    # install the "best" available Twisted reactor
    #
    from autobahn.twisted.choosereactor import install_reactor
    reactor = install_reactor()
    log.msg("Running on reactor {}".format(reactor))

    extra = {
        'id': args.id
    }

    runner = ApplicationRunner(url=args.router, realm=args.realm, extra=extra, debug=args.debug)
    runner.run(PiMonitor)
