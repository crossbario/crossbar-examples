from autobahn.twisted.wamp import ApplicationSession
from autobahn.twisted.wamp import ApplicationRunner


class MyComponent(ApplicationSession):

    def onJoin(self, details):
        print('Session joined. Configuration: {}'.format(self.config.extra))


# This is for running the component manually (not being started by Crossbar.io)
if __name__ == '__main__':
    extra = {
        'foo': 'bar',
        'baz': 23
    }
    runner = ApplicationRunner(url='ws://localhost:8080/ws', realm='realm1', extra=extra)
    runner.run(MyComponent)
