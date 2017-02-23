from twisted.internet.defer import inlineCallbacks
from twisted.internet.task import LoopingCall
from autobahn.twisted.wamp import ApplicationSession

def add2(a, b):
    print('add2 called: {} {}'.format(a, b))
    return a + b

def validate_int(num):
    print('validate_int called: {}'.format(num))
    try:
        int(num)
        return True
    except ValueError:
        return False

NODES = {
    u'node1': {
        u'workers': {
            u'worker1': {
                u'type': u'router'
            },
            u'worker2': {
                u'type': u'guest'
            }
        }
    },
    u'mynode': {
        u'workers': {
            u'myrouter': {
                u'type': u'router'
            },
            u'guest01': {
                u'type': u'guest'
            },
            u'guest02': {
                u'type': u'guest'
            },
            u'guest03': {
                u'type': u'guest'
            }
        }
    },
    u'foo23': {
        u'workers': {
            u'w23-1': {
                u'type': u'router'
            },
            u'w23-2': {
                u'type': u'guest'
            }
        }
    }
}

from autobahn.util import utcnow
from autobahn.wamp import register

class Backend(ApplicationSession):

    @inlineCallbacks
    def onJoin(self, details):
        self._started = utcnow()

        self._tick = 1

        def tick():
            self.publish(u'com.example.tick', self._tick)
            self._tick += 1

        c = LoopingCall(tick)
        c.start(1)

        yield self.register(add2, u'com.example.add2')
        yield self.register(validate_int, u'com.example.validate_int')

        yield self.register(self)

        self.log.info('backend ready!')

    @register(u'com.example.list_nodes')
    def list_nodes(self, verbose=False):
        return sorted(NODES.keys())

    @register(u'com.example.list_workers')
    def list_workers(self, node, verbose=False):
        if node in NODES:
            return sorted(NODES[node][u'workers'].keys())
        else:
            return None

    @register(u'com.example.show_fabric')
    def show_fabric(self, verbose=False):
        res = {
            u'version': u'17.01.23',
            u'now': utcnow(),
            u'started': self._started,
            u'tick': self._tick
        }
        return res

    @register(u'com.example.show_node')
    def show_node(self, node, verbose=False):
        return NODES.get(node, None)

    @register(u'com.example.show_worker')
    def show_worker(self, node, worker, verbose=False):
        if node in NODES:
            workers = NODES[node][u'workers']
            if worker in workers:
                return workers[worker]
