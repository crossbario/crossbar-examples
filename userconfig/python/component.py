from autobahn.twisted.wamp import ApplicationSession
from autobahn.twisted.wamp import ApplicationRunner


class MyComponent(ApplicationSession):

    def onJoin(self, details):
        print('Session joined. Configuration: {}'.format(self.config.extra))


# This is for running the component manually (not being started by Crossbar.io)
if __name__ == '__main__':
    extra = {
        u'foo': u'bar',
        u'baz': 23
    }
    runner = ApplicationRunner(url=u'ws://localhost:8080/ws', realm=u'realm1', extra=extra)
    runner.run(MyComponent)
