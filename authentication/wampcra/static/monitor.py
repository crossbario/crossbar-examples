from pprint import pformat

import txaio
txaio.use_twisted()

import argparse
from autobahn.util import hlid, hlval, hltype

from twisted.internet.defer import inlineCallbacks

from autobahn.twisted.wamp import ApplicationRunner
from autobahn.twisted.wamp import ApplicationSession


class MyMonitor(ApplicationSession):

    def onConnect(self):
        self.log.info('{func}: client session connected, now joining realm "{realm}" ..',
                      func=hltype(self.onConnect), realm=hlid(self.config.realm))
        self.join(self.config.realm)

    @inlineCallbacks
    def onJoin(self, details):
        self.log.info('{func}: client session joined:\n{details}',
                      func=hltype(self.onJoin), details=pformat(details))

        sessions = yield self.call('wamp.session.list')
        for session_id in sessions:
            try:
                session_info = yield self.call('wamp.session.get', session_id)
                self.log.info('{func}: session_info=\n{session_info}',
                              func=hltype(self.onJoin), session_info=pformat(session_info))
            except:
                self.log.failure()

        def on_session_join(session_info):
            self.log.info('{func}: new session joined, session_info=\n{session_info}',
                          func=hltype(on_session_join), session_info=pformat(session_info))

        yield self.subscribe(on_session_join, 'wamp.session.on_join')

        def on_session_leave(session_id):
            self.log.info('{func}: existing session left, session_id={session_id}',
                          func=hltype(on_session_join), session_id=hlid(session_id))

        yield self.subscribe(on_session_leave, 'wamp.session.on_leave')


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--debug', action='store_true', help='Enable debug output.')
    parser.add_argument('--url', dest='url', type=str, default='ws://192.168.40.121:8080/ws',
                        help='The router URL (default: "ws://localhost:8080/ws").')
    parser.add_argument('--realm', dest='realm', type=str, default='realm1',
                        help='The realm to join (default: "realm1").')

    args = parser.parse_args()

    if args.debug:
        txaio.start_logging(level='debug')
    else:
        txaio.start_logging(level='info')

    runner = ApplicationRunner(url=args.url, realm=args.realm)
    runner.run(MyMonitor, auto_reconnect=True)
