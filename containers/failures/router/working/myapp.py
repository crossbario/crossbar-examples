import txaio
txaio.use_twisted()

from txaio import make_logger
from twisted.internet import reactor
from twisted.internet.defer import inlineCallbacks
from autobahn.twisted.wamp import ApplicationSession


class MySession(ApplicationSession):

    log = make_logger()

    def __init__(self, config):
        self.log.info('MySession.__init__(config={config})', config=config)
        ApplicationSession.__init__(self, config)

    def onJoin(self, details):
        self.log.info('MySession.onJoin(details={details})', details=details)
        self.log.info('sleeping for 3s before leaving ..')

        @inlineCallbacks
        def shutdown():
            self.log.info('shutting down ..')
            try:
                shutting_down = yield self.config.controller.call('crossbar.shutdown')
            except:
                self.log.failure()
            else:
                self.log.info('shutdown in progress: {shutting_down}', shutting_down=shutting_down)
            self.leave()

        reactor.callLater(3, shutdown)

    def onLeave(self, details):
        self.log.info('MySession.onLeave(details={details})', details=details)
        ApplicationSession.onLeave(self, details)
