import sys
import mraa
from twisted.internet.defer import inlineCallbacks
from twisted.internet.task import LoopingCall
from autobahn.twisted.wamp import ApplicationSession
from autobahn import wamp

# adjust this for your setup:
LED1_PIN = 11   # O0 (used as digital) on Arduino Tinkershield
BTN1_PIN = 14   # I0 (used as digital) on Arduino Tinkershield
POT1_PIN = 1    # I1 (used as analog) on Arduino Tinkershield
ROUTER = "ws://192.168.1.130:8080/ws"
REALM = "realm1"
BASE_URI = u"io.crossbar.demo.edison.tutorial3"


class MyEdisonBridgeSession(ApplicationSession):

    @inlineCallbacks
    def onJoin(self, details):
        print("Session connected")

        self._last = None
        self._led = False

        self._led1 = mraa.Gpio(LED1_PIN)
        self._led1.dir(mraa.DIR_OUT)        

        self._btn1 = mraa.Gpio(BTN1_PIN)
        self._btn1.dir(mraa.DIR_IN)
        
        self._pot1 = mraa.Aio(POT1_PIN)

        def loop():
            values = [self._btn1.read(), self._pot1.read()]
            if self._last is None:
                self._last = values
                changed = True
            else:
                changed = False

                if values[0] != self._last[0]:
                    changed = True
                if abs(values[1] - self._last[1]) > 4:
                    changed = True

                if changed:
                    print(values)
                    self.publish(u"{}.on_sensors".format(BASE_URI), values)
                    self._last = values

        self._loop = LoopingCall(loop)
        self._loop.start(0.05)

        yield self.register(self)
        print("Procedures registered.")

        print("Bridge ready!")

    def onLeave(self, details):
        if self._loop:
            self._loop.stop()
        self.disconnect()

    @wamp.register(u"{}.get_sensors".format(BASE_URI))
    def get_sensor_vals(self):
        return self._last

    @wamp.register(u"{}.set_led".format(BASE_URI))
    def set_led(self, value):
        if value:
            if not self._led:
                self._led1.write(1)
                self._led = True
                self.publish(u"{}.on_led".format(BASE_URI), self._led)
                return True
            else:
                return False
        else:
            if self._led:
                self._led1.write(0)
                self._led = False
                self.publish(u"{}.on_led".format(BASE_URI), self._led)
                return True
            else:
                return False

    @wamp.register(u"{}.get_led".format(BASE_URI))
    def get_led(self):
        return self._led


if __name__ == '__main__':

    import sys
    from twisted.python import log
    log.startLogging(sys.stdout)

    from twisted.internet import reactor
    print("Using Twisted reactor {0}".format(reactor.__class__))

    from autobahn.twisted.wamp import ApplicationRunner

    runner = ApplicationRunner(ROUTER, REALM)
    runner.run(MyEdisonBridgeSession)
