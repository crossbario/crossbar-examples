###############################################################################
#
# The MIT License (MIT)
#
# Copyright (c) Tavendo GmbH
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
###############################################################################

from twisted.internet.defer import inlineCallbacks

from autobahn import wamp
from autobahn.twisted.wamp import ApplicationSession


class WpadSeries(ApplicationSession):

    """
    MCU WAMP application component.
    """

    @inlineCallbacks
    def onJoin(self, details):
        self._id = 1
        self._data = {}
        yield self.register(self)
        print("WPad series store ready!")

    @wamp.register(u'io.crossbar.demo.wpad.store_series')
    def store_series(self, data):
        print data
        assert(type(data) == dict)
        n = None
        for series in data.values():
            assert(type(series) == list)
            if n is None:
                n = len(series)
            else:
                assert(len(series) == n)
            for value in series:
                assert(value is None or type(value) in [int, float])
        self._data[self._id] = data
        self.publish(u'io.crossbar.demo.wpad.on_series_stored', self._id, len(data), n)
        self._id += 1
        return self._id - 1

    @wamp.register(u'io.crossbar.demo.wpad.get_series_count')
    def get_series_count(self):
        return len(self._data)

    @wamp.register(u'io.crossbar.demo.wpad.get_series')
    def get_series(self, series_id):
        return self._data.get(series_id, None)


if __name__ == '__main__':

    import sys
    import argparse

    # parse command line arguments
    ##
    parser = argparse.ArgumentParser()

    parser.add_argument("--router", type=str, default='ws://localhost:8080/ws',
                        help='Connect to this WAMP router.')

    parser.add_argument("--realm", type=str, default='realm1',
                        help='Realm to attach to.')

    args = parser.parse_args()

    from twisted.python import log
    log.startLogging(sys.stdout)

    # import Twisted reactor
    #
    from twisted.internet import reactor
    print("Using Twisted reactor {0}".format(reactor.__class__))

    # run WAMP application component
    #
    from autobahn.twisted.wamp import ApplicationRunner

    runner = ApplicationRunner(args.router, args.realm, extra={})

    # start the component and the Twisted reactor ..
    #
    runner.run(WpadSeries)
