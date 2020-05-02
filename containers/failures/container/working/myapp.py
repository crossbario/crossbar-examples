import txaio
txaio.use_twisted()

from txaio import make_logger
from twisted.internet import reactor
from autobahn.twisted.wamp import ApplicationSession


class MySession(ApplicationSession):

    log = make_logger()

    def __init__(self, config):
        self.log.info('MySession.__init__(config={config})', config=config)
        ApplicationSession.__init__(self, config)

    def onJoin(self, details):
        self.log.info('MySession.onJoin(details={details})', details=details)
        self.log.info('sleeping for 3s before leaving ..')
        reactor.callLater(3, self.leave)
