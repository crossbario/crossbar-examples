# Copyright (C) Tavendo GmbH. Open-source licensed under the
# MIT License (http://opensource.org/licenses/MIT)

import re
import sys
import argparse

from twisted.python import log
from twisted.internet.utils import getProcessOutput
from twisted.internet.defer import inlineCallbacks

from autobahn import wamp
from autobahn.twisted.wamp import ApplicationSession
from autobahn.twisted.wamp import ApplicationRunner


class FliteBridge(ApplicationSession):
    """
    Connects Flite text-to-speech engine to WAMP.
    """

    @inlineCallbacks
    def onJoin(self, details):
        log.msg("FliteBridge connected.")

        extra = self.config.extra

        self._id = extra['id']
        self._flite = extra['flite']
        self._voice = extra.get('voice', 'slt')

        self._is_busy = False
        for proc in [self.say, self.is_busy]:
            uri = u'com.example.device.{}.tts.{}'.format(self._id, proc.__name__)
            yield self.register(proc, uri)
            log.msg("Registered {}".format(uri))

        log.msg("FliteBridge ready.")

    @inlineCallbacks
    def say(self, text):
        """
        Speak text.
        """
        if self._is_busy:
            raise Exception("already talking")
        else:
            # mark TTS engine as busy and publish event
            self._is_busy = True
            self.publish(u'com.example.device.{}.tts.on_speech_start'.format(self._id), text)

            # start TTS
            yield getProcessOutput(self._flite, ['-voice', self._voice, '-t', text])

            # mark TTS engine as free and publish event
            self.publish(u'com.example.device.{}.tts.on_speech_end'.format(self._id))
            self._is_busy = False

    def is_busy(self):
        """
        Check if TTS engine is currently busy speaking.
        """
        return self._is_busy


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
                        help='The Device ID to use. Default is to use the RaspberryPi Serial Number')

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
        'id': args.id,
        'flite': '/usr/bin/flite',
        'voice': 'slt'
    }

    runner = ApplicationRunner(url=args.router, realm=args.realm, extra=extra, debug=args.debug)
    runner.run(FliteBridge)
