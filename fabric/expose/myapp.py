import random
from twisted.internet.defer import inlineCallbacks
from autobahn.twisted.wamp import ApplicationSession

class MySession(ApplicationSession):

    @inlineCallbacks
    def onJoin(self, details):
        self.log.info('Session: {}'.format(details))

        if self.config.shared:
            if 'dbpool' not in self.config.shared:
                self.config.shared['dbpool'] = random.random()

        print('config: {}'.format(self.config))

        if self.config.controller:
            yield self.test0()
            #yield self.test1()
            #yield self.test2()
            #yield self.test3()

    @inlineCallbacks
    def test0(self):
        print(self.config.controller)

        res = yield self.config.controller.call(u'crossbar.get_info')
        print(res)

    @inlineCallbacks
    def test1(self):
        print(self.config.controller)

        res = yield self.config.controller.call(u'crossbar.start_container', u'foo-container')
        print(res)

    @inlineCallbacks
    def test2(self):
        res = yield self.config.controller.call(u'crossbar.worker.worker-002.get_container_components')
        n = len(res)
        print('{} components running'.format(n))
        n += 1

        if n < 1000:
            comp_id = u'comp-{}'.format(n)
            comp_config = {
                u"type": u"class",
                u"classname": u"myapp.MySession",
                u"realm": u"realm1",
                u"transport": {
                    u"type": u"websocket",
                    u"endpoint": {
                        u"type": u"tcp",
                        u"host": u"127.0.0.1",
                        u"port": 8080
                    },
                    u"url": u"ws://127.0.0.1:8080/ws"
                }
            }
            res = yield self.config.controller.call(u'crossbar.worker.worker-002.start_container_component', comp_id, comp_config)

    @inlineCallbacks
    def test3(self):
        print(self.config.controller)

        realm_id = u'realm2'
        realm_config = {
            u'name': u'realm2'
        }

        res = yield self.config.controller.call(u'crossbar.worker.worker-001.start_router_realm', realm_id, realm_config)
        print(res)

        res = yield self.config.controller.call(u'crossbar.get_info')
        print(res)

