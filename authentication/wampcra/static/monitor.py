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

        @inlineCallbacks
        def on_session_join(session_info):
            self.log.info('{func}: new session joined, session_info=\n{session_info}',
                          func=hltype(on_session_join), session_info=pformat(session_info))

            # verify the getter API responds with the same data that we got sent in the event already
            session_id = session_info.get('session', None)
            if session_id:
                try:
                    _session_info = yield self.call('wamp.session.get', session_id)

                    # FIXME
                    for attr in ['realm', 'serializer', 'resumable', 'resume_token', 'resumed']:
                        if attr in _session_info:
                            del _session_info[attr]

                    if session_info == _session_info:
                        self.log.info('{func}: ok, event data identical to getter API!', func=hltype(on_session_join))
                    else:
                        self.log.warn('{func}: event data mismatch to getter API!\nEvent:\n{session_info_event}\nCall:\n{session_info_call}',
                                      session_info_event=pformat(session_info),
                                      session_info_call=pformat(_session_info),
                                      func=hltype(on_session_join))
                except:
                    self.log.failure()

        yield self.subscribe(on_session_join, 'wamp.session.on_join')

        @inlineCallbacks
        def on_session_leave(session_id):
            self.log.info('{func}: existing session left, session_id={session_id}',
                          func=hltype(on_session_join), session_id=hlid(session_id))

            # ApplicationError(error=<wamp.error.no_such_session)
            if session_id:
                try:
                    _session_info = yield self.call('wamp.session.get', session_id)
                    if session_info == _session_info:
                        self.log.info('{func}: ok, event data identical to getter API', func=hltype(on_session_join))
                except:
                    self.log.failure()

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
