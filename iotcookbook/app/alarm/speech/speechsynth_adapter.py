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


class SpeechSynthAdapter(ApplicationSession):
    """
    Connects the Flite text-to-speech engine to WAMP.
    """

    @inlineCallbacks
    def onJoin(self, details):
        # the component has now joined the realm on the WAMP router
        log.msg("SpeechSynthAdapter connected.")

        # get custom configuration
        extra = self.config.extra

        # Device ID and auxiliary info
        self._id = extra['id']
        self._flite = extra['flite']
        self._voice = extra.get('voice', 'slt')

        # becomes true when currently speaking
        self._is_busy = False

        # register methods on this object for remote calling via WAMP
        for proc in [self.say, self.is_busy]:
            uri = u'io.crossbar.examples.iotcookbook.alarmapp.{}.speechsynth.{}'.format(self._id, proc.__name__)
            yield self.register(proc, uri)
            log.msg("SpeechSynthAdapter registered procedure {}".format(uri))

        # signal we are done with initializing our component
        self.publish(u'io.crossbar.examples.iotcookbook.alarmapp.{}.speechsynth.on_ready'.format(self._id))
        log.msg("SpeechSynthAdapter ready.")

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
            self.publish(u'io.crossbar.examples.iotcookbook.alarmapp.{}.speechsynth.on_speech_start'.format(self._id), text)

            # start TTS
            yield getProcessOutput(self._flite, ['-voice', self._voice, '-t', text])

            # mark TTS engine as free and publish event
            self._is_busy = False
            self.publish(u'io.crossbar.examples.iotcookbook.alarmapp.{}.speechsynth.on_speech_end'.format(self._id))

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

    # start logging to stdout
    #
    log.startLogging(sys.stdout)

    # get the Pi's serial number (allow override from command line)
    #
    if args.id is None:
        args.id = get_serial()
    log.msg("SpeechSynthAdapter starting with Device ID {} ...".format(args.id))

    # install the "best" available Twisted reactor
    #
    from autobahn.twisted.choosereactor import install_reactor
    reactor = install_reactor()
    log.msg("Running on reactor {}".format(reactor))

    # custom configuration data
    #
    extra = {
        # device ID
        'id': args.id,

        # full path to Flite executable
        'flite': '/usr/bin/flite',

        # voice to use with Flite (list: flite -lv)
        'voice': 'slt'
    }

    # create and start app runner for our app component ..
    #
    runner = ApplicationRunner(url=args.router, realm=args.realm, extra=extra, debug=args.debug)
    runner.run(SpeechSynthAdapter)
