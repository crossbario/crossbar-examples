import os
import threading

import txaio
txaio.use_twisted()
from txaio import make_logger

from twisted.internet.defer import inlineCallbacks

from autobahn.wamp.types import CallDetails, RegisterOptions, EventDetails, SubscribeOptions
from autobahn.twisted.wamp import ApplicationSession
from autobahn.wamp.exception import InvalidUriError


INVALID_URI = "crossbarfabriccenter.node.{'oid': '4752c752-a128-4ae4-a041-84208eabe49d'}.get_docker_images"


class MyCallerCallee(ApplicationSession):

    log = make_logger()

    def __init__(self, config):
        self.ident = '{}:{}'.format(os.getpid(), threading.get_ident())

        self.log.info('{klass}[{ident}].__init__(config={config})',
                      klass=self.__class__.__name__, ident=self.ident, config=str(config))

        ApplicationSession.__init__(self, config)

    @inlineCallbacks
    def onJoin(self, details):
        self.log.info('{klass}[{ident}].onJoin(details={details})',
                      klass=self.__class__.__name__, ident=self.ident, details=details)

        # REGISTER
        try:
            yield self.register(self.echo, INVALID_URI, options=RegisterOptions(invoke='roundrobin'))
        except Exception as e:
            self.log.failure()

            if isinstance(e, InvalidUriError):
                self.log.info('OK: REGISTER got expected exception InvalidUriError!')
            else:
                self.log.warn('ERROR: REGISTER got unexpected exception "{err}"', err=str(e))
        else:
            self.log.warn('ERROR: REGISTER expected a InvalidUriError exception - but got none! ')

        # CALL
        try:
            yield self.call(INVALID_URI, b'\xff' * 16)
        except Exception as e:
            self.log.failure()

            if isinstance(e, InvalidUriError):
                self.log.info('OK: CALL got expected exception InvalidUriError!')
            else:
                self.log.warn('ERROR: CALL got unexpected exception "{err}"', err=str(e))
        else:
            self.log.warn('ERROR: CALL expected a InvalidUriError exception - but got none! ')

        # SUBSCRIBE
        try:
            yield self.subscribe(self.on_topic1, INVALID_URI, options=SubscribeOptions(details=True))
        except Exception as e:
            self.log.failure()

            if isinstance(e, InvalidUriError):
                self.log.info('OK: SUBSCRIBE got expected exception InvalidUriError!')
            else:
                self.log.warn('ERROR: SUBSCRIBE got unexpected exception "{err}"', err=str(e))
        else:
            self.log.warn('ERROR: SUBSCRIBE expected a InvalidUriError exception - but got none! ')

        # PUBLISH
        try:
            yield self.publish(INVALID_URI, b'\xff' * 16)
        except Exception as e:
            self.log.failure()

            if isinstance(e, InvalidUriError):
                self.log.info('OK: PUBLISH got expected exception InvalidUriError!')
            else:
                self.log.warn('ERROR: PUBLISH got unexpected exception "{err}"', err=str(e))
        else:
            self.log.warn('ERROR: PUBLISH expected a InvalidUriError exception - but got none! ')

        # OK, all done!
        yield self.leave()

    def echo(self, data, details=None):
        assert type(data) == bytes, '"data" must be bytes, but was {}'.format(type(data))
        assert details is None or isinstance(details, CallDetails), '"details" must be CallDetails, but was {}'.format(type(details))

        self.log.info('{klass}[{ident}].echo(data={dlen}, details={details}): echo return {dlen} bytes',
                      klass=self.__class__.__name__,
                      ident=self.ident,
                      details=details,
                      dlen=len(data))

        return data

    def on_topic1(self, data, details=None):
        assert type(data) == bytes, '"data" must be bytes, but was {}'.format(type(data))
        assert details is None or isinstance(details, EventDetails), '"details" must be EventDetails, but was {}'.format(type(details))

        self.log.info('{klass}[{ident}].on_topic1(data={dlen}, details={details})',
                      klass=self.__class__.__name__,
                      ident=self.ident,
                      details=details,
                      dlen=len(data))
