import six
import argparse
from pprint import pformat

import txaio
txaio.use_twisted()

from autobahn.twisted.wamp import ApplicationSession, ApplicationRunner


class ClientSession(ApplicationSession):

    async def onJoin(self, details):
        print('MONITOR session joined: {}'.format(details))

        xbr_config = self.config.extra['xbr']

        # {'market-url': '', 'market-realm': '', 'delegate-key': '../.xbr.key'}
        print(xbr_config)

        def on_session_join(session_details):
            self.log.info('>>>>>> MONITOR : session joined\n{session_details}\n',
                          session_details=pformat(session_details))

        await self.subscribe(on_session_join, 'wamp.session.on_join')

        def on_session_stats(session_details, stats):
            self.log.info('>>>>>> MONITOR : session stats\n{session_details}\n{stats}\n',
                          session_details=pformat(session_details), stats=pformat(stats))

        await self.subscribe(on_session_stats, 'wamp.session.on_stats')

        def on_session_leave(session_id):
            self.log.info('>>>>>> MONITOR : session {session_id} left',
                          session_id=session_id)

        await self.subscribe(on_session_leave, 'wamp.session.on_leave')


if __name__ == '__main__':

   parser = argparse.ArgumentParser()

   parser.add_argument('-d',
                       '--debug',
                       action='store_true',
                       help='Enable debug output.')

   parser.add_argument('--url',
                       dest='url',
                       type=str,
                       default="ws://localhost:8080/ws",
                       help='The router URL (default: "ws://localhost:8080/ws").')

   parser.add_argument('--realm',
                       dest='realm',
                       type=str,
                       default="realm1",
                       help='The realm to join (default: "realm1").')

   args = parser.parse_args()

   if args.debug:
      txaio.start_logging(level='debug')
   else:
      txaio.start_logging(level='info')

   runner = ApplicationRunner(url=args.url, realm=args.realm)
   runner.run(ClientSession, auto_reconnect=True)
