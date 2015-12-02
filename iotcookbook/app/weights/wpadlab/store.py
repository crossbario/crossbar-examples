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

import shelve

from twisted.internet.defer import inlineCallbacks

from autobahn import wamp
from autobahn.twisted.wamp import ApplicationSession


class WpadObjectStore(ApplicationSession):

    """
    MCU WAMP application component.
    """

    @inlineCallbacks
    def onJoin(self, details):
        print("Session attached")

        # poor man's key-value database
        self._store = shelve.open(self.config.extra['database'])

        # expose object store WAMP API
        yield self.register(self)

        print("WPad object store ready!")

    def onLeave(self, details):
        print("Session detached")
        self._store.close()
        self.disconnect()

    @wamp.register(u'io.crossbar.demo.wpad.objstore.save')
    def save(self, obj_type, obj_data):
        assert(type(obj_type) in (str, unicode))

        next_id = "{}.{}".format("next_id", obj_type)

        if next_id not in self._store:
            self._store[next_id] = 1
            self._store.sync()

        obj_id = self._store[next_id]
        self._store[next_id] = obj_id + 1
        self._store.sync()

        self._store["{}.{}".format(obj_type, obj_id)] = obj_data

        self.publish(u'io.crossbar.demo.wpad.objstore.on_save', obj_type, obj_id)

        return obj_id

    @wamp.register(u'io.crossbar.demo.wpad.objstore.get')
    def get(self, obj_type, obj_id):
        if type(obj_id) == float:
            obj_id = int(obj_id)
        assert(type(obj_id) == int)
        obj_id = "{}.{}".format(obj_type, obj_id)
        if obj_id in self._store:
            return self._store[obj_id]
        else:
            return None

    @wamp.register(u'io.crossbar.demo.wpad.objstore.count')
    def count(self, obj_type=None):
        return len(self._store)


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

    extra = {
        "database": "wpad.dat",
        "debug": True
    }

    runner = ApplicationRunner(args.router, args.realm, extra=extra)

    # start the component and the Twisted reactor ..
    #
    runner.run(WpadObjectStore)
