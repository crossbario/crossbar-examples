from twisted.internet.defer import inlineCallbacks
from autobahn.twisted.util import sleep
import util

NODE_ID = u'node1'
WORKER_ID = u'myworker'
REALM_ID = u'myrealm'
REALM_CONFIG = {
    u'name': REALM_ID
}
ROLE_CONFIG = {
    u"name": u"dummy",
    u"permissions": [
        {
            u"uri": u"com.example.dummy",
            u"match": u"prefix",
            u"allow": {
                u"call": True
            }
        }
    ]
}
TRANSPORT_ID = u'mytransport'
TRANSPORT_CONFIG = {
    u'type': u'websocket',
    u'endpoint': {
        u'type': u'tcp',
        u'port': 9000
    }
}

@inlineCallbacks
def main(session, details):
    try:
        nodes = yield session.call(u'com.crossbario.cdc.management.get_nodes@1')
        workers_started = []

        for node_id in nodes:
            node = yield session.call(u'com.crossbario.cdc.management.get_node_status@1', node_id)
            node_status = node[u'status']

            session.log.info('provisioned node "{node_id}" in status "{node_status}"', node_id=node_id, node_status=node_status)

            if node_status != u'online':
                session.log.info('node not online - skipping for test')
                continue

            workers = yield session.call(u'com.crossbario.cdc.remote.get_workers@1', node_id)
            if WORKER_ID in workers:
                stopped = yield session.call(u'com.crossbario.cdc.remote.stop_worker@1', node_id, WORKER_ID)
                session.log.info('worker stopped')

            started = yield session.call(u'com.crossbario.cdc.remote.start_router@1', node_id, WORKER_ID)
            session.log.info('worker started')

            workers_started.append((node_id, WORKER_ID))

            started = yield session.call(u'com.crossbario.cdc.remote.start_router_realm@1', node_id, WORKER_ID, REALM_ID, REALM_CONFIG)
            session.log.info('realm started')

            for x in range(10):
                role_id = u'user-{}'.format(x)
                ROLE_CONFIG[u'name'] = role_id
                ROLE_CONFIG[u'permissions'][0][u'uri'] = u'com.example.{}'.format(role_id)
                started = yield session.call(u'com.crossbario.cdc.remote.start_realm_role@1', node_id, WORKER_ID, REALM_ID, role_id, ROLE_CONFIG)
                session.log.info('role started')

            started = yield session.call(u'com.crossbario.cdc.remote.start_router_transport@1', node_id, WORKER_ID, TRANSPORT_ID, TRANSPORT_CONFIG)
            session.log.info('transport started')
            TRANSPORT_CONFIG[u'endpoint'][u'port'] += 1

        session.log.info('sleeping ..')
        yield sleep(5)

        for node_id, worker_id in workers_started:
            yield session.call(u'com.crossbario.cdc.remote.stop_worker@1', node_id, worker_id)
            session.log.info('worker stopped')
    except:
        session.log.failure()

util.run(main)
