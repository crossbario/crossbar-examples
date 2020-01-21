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
    'node1': {
        'workers': {
            'worker1': {
                'type': 'router'
            },
            'worker2': {
                'type': 'guest'
            }
        }
    },
    'mynode': {
        'workers': {
            'myrouter': {
                'type': 'router'
            },
            'guest01': {
                'type': 'guest'
            },
            'guest02': {
                'type': 'guest'
            },
            'guest03': {
                'type': 'guest'
            }
        }
    },
    'foo23': {
        'workers': {
            'w23-1': {
                'type': 'router'
            },
            'w23-2': {
                'type': 'guest'
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
            self.publish('com.example.tick', self._tick)
            self._tick += 1

        c = LoopingCall(tick)
        c.start(1)

        yield self.register(add2, 'com.example.add2')
        yield self.register(validate_int, 'com.example.validate_int')

        yield self.register(self)

        self.log.info('backend ready!')

    @register('com.example.list_nodes')
    def list_nodes(self, verbose=False):
        return sorted(NODES.keys())

    @register('com.example.list_workers')
    def list_workers(self, node, verbose=False):
        if node in NODES:
            return sorted(NODES[node]['workers'].keys())
        else:
            return None

    @register('com.example.show_fabric')
    def show_fabric(self, verbose=False):
        res = {
            'version': '17.01.23',
            'now': utcnow(),
            'started': self._started,
            'tick': self._tick
        }
        return res

    @register('com.example.show_node')
    def show_node(self, node, verbose=False):
        return NODES.get(node, None)

    @register('com.example.show_worker')
    def show_worker(self, node, worker, verbose=False):
        if node in NODES:
            workers = NODES[node]['workers']
            if worker in workers:
                return workers[worker]
