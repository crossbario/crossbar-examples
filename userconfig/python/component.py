from autobahn.twisted.wamp import ApplicationSession
from autobahn.twisted.wamp import ApplicationRunner


class MyComponent(ApplicationSession):

    def onJoin(self, details):
        print("Session joined. Configuration: {}".format(self.config.extra))


if __name__ == '__main__':

    # This is for running the component manually (not being started by Crossbar.io)

    extra = {
        "foo": "bar",
        "baz": 23
    }
    runner = ApplicationRunner(url=u"ws://localhost:8080/ws", realm=u"realm1", extra=extra)
    runner.run(MyComponent)
