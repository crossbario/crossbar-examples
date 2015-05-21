# Copyright (C) Tavendo GmbH. Open-source licensed under the
# MIT License (http://opensource.org/licenses/MIT)

import re
import sys
import argparse
import pygame
import os
import treq

from twisted.python import log
from twisted.internet.utils import getProcessOutput
from twisted.internet.defer import inlineCallbacks



from autobahn import wamp
from autobahn.twisted.wamp import ApplicationSession
from autobahn.twisted.wamp import ApplicationRunner


class AudioOutputAdapter(ApplicationSession):
    """
    Connects the pygame mixer to WAMP.
    """

    @inlineCallbacks
    def onJoin(self, details):
        # the component has now joined the realm on the WAMP router
        log.msg("AudioOutputAdapter connected.")

        # get custom configuration
        extra = self.config.extra

        # Device ID and auxiliary info
        self._id = extra['id']

        # set up the pygame mixer we use for playing sounds
        pygame.mixer.init()
        
        # get the samples we've stored locally
        # and create pygame Sound objects from them
        samples = os.listdir("samples")
        self.sampleObjects = {}
        for idx, sample in enumerate(samples):
            # get the sample name without the file type ending (if any)
            if len(sample.split(".")) > 1:
                sample_name = sample.split(".")[0]
            else:
                sample_name = sample
            self.sampleObjects[sample_name] = pygame.mixer.Sound("./samples/" + sample)
            print "sample " + sample_name + " added"

        # register methods on this object for remote calling via WAMP
        for proc in [self.trigger_sample, self.stop_sample, self.add_sample]:
            uri = u'io.crossbar.examples.iot.devices.pi.{}.audioout.{}'.format(self._id, proc.__name__)
            yield self.register(proc, uri)
            log.msg("AudioOutputAdapter registered procedure {}".format(uri))

        # signal we are done with initializing our component
        self.publish(u'io.crossbar.examples.iot.devices.pi.{}.audioout.on_ready'.format(self._id))
        log.msg("AudioOutputAdapter ready.")

    def trigger_sample(self, sample_name):
        """
        Play ogg or WAV audio file
        """
        self.sampleObjects[sample_name].play()


    def stop_sample(self, sample_name):
        """
        Stop a currently playing sample
        """
        self.sampleObjects[sample_name].stop()

    @inlineCallbacks
    def add_sample(self, sample_url, sample_name):
        """
        add a sample from an URL
        """
        sample_url = sample_url.encode("ascii", "ignore")
        sample_type = sample_url.split(".")[-1]
        if sample_type.lower() != "wav" and sample_type.lower() != "ogg":
            print "unknown sample type?"

        # download the sample
        res = yield treq.get(sample_url)
        content = yield res.content()
        # write to disk
        with open("samples/" + sample_name + "." + sample_type, "w") as new_sample:
            new_sample.write(content)
        # add to our current samples
        self.sampleObjects[sample_name] = pygame.mixer.Sound("./samples/" + sample_name + "." + sample_type)
        print "sample %s added" % (sample_name)

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

    parser.add_argument("--router", type=unicode, default=u"ws://192.168.1.134:8080/ws",
                        help='URL of WAMP router to connect to.')

    parser.add_argument("--realm", type=unicode, default=u"iot_cookbook",
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
    log.msg("AudioOutputAdapter starting with Device ID {} ...".format(args.id))

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
    }

    # create and start app runner for our app component ..
    #
    runner = ApplicationRunner(url=args.router, realm=args.realm, extra=extra, debug=args.debug)
    runner.run(AudioOutputAdapter)
