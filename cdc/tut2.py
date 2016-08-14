from twisted.internet.defer import inlineCallbacks
import util

@inlineCallbacks
def main(session, details):
    try:
        # get list of node_ids of Crossbar.io nodes provisioned on this management realm
        nodes = yield session.call(u'com.crossbario.cdc.management.get_nodes@1')

        for node_id in nodes:
            # get node status given node_id
            node_status = yield session.call(u'com.crossbario.cdc.management.get_node_status@1', node_id)
            session.log.info('Node "{node_id}" status: {node_status}', node_id=node_id, node_status=node_status)

            if node_status[u'status'] == u'online':
                # if the node is online, get node controller status
                node_info = yield session.call(u'com.crossbario.cdc.remote.get_controller_info@1', node_id)
                session.log.info('Node "{node_id}" info: {node_info}', node_id=node_id, node_info=node_info)
    except:
        session.log.failure()

util.run(main)
