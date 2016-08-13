from twisted.internet.defer import inlineCallbacks
import util

@inlineCallbacks
def main(session, details):
    try:
        nodes = yield session.call(u'com.crossbario.cdc.management.get_nodes@1')
    except:
        session.log.failure()
    else:
        session.log.info('Nodes on management realm "{realm}"', realm=details.realm)
        for node_id in nodes:
            node_status = yield session.call(u'com.crossbario.cdc.management.get_node_status@1', node_id)
            session.log.info('Node "{node_id}": {node_status}', node_id=node_id, node_status=node_status)

util.run(main)
