from __future__ import print_function

import os
import json
import random

from twisted.python import log
import sys
log.startLogging(sys.stdout)

from twisted.internet import reactor
from autobahn.twisted.wamp import ApplicationSession, ApplicationRunner


def random_event():
    """
    make a random _network_ event of the form:
    {"parm": "192.168.6.108", "verb": "up", "noun": "endpoint", "level": "info"}
    """

    d = {}
    d['noun'] = random.choice( ['endpoint', 'router', 'link'] )
    d['parm'] = "192.168.%d.%d" % (random.randrange(1,10), random.randrange(1,250))
    d['verb'] = random.choice( ['down', 'up'] )
    d['level'] = 'info' if d['verb'] == 'up' else 'warning'

    return json.dumps( d )


class AppSession( ApplicationSession ):
    """
    this object connects to the crossbar router
    """

    def onJoin(self, details):
        log.msg("netmonitor session attached")

        self._parent = self.config.extra['parent'] # set via extra kw below
        self._parent.start(self)


class NetMonitor( object ):

    def __init__( self, reactor, ws ):
        self._reactor = reactor
        self._ws = ws

        self._runner = ApplicationRunner( self._ws, u"realm1",
                    debug_wamp=False, # optional; log many WAMP details
                    debug=False,      # optional; log even more details
                    extra=dict(parent=self)
                )
        self._runner.run( AppSession, start_reactor=False )

    def start( self, session ):
        self._session = session
        self._reactor.callLater( 0, self.pub_event )

    def pub_event( self ):
        e = random_event()
        self._session.publish('netmonitor.event', e )

        self._reactor.callLater( 5, self.pub_event )

nm = NetMonitor( reactor, os.environ['WS'] )
reactor.run()
