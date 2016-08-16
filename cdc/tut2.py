from twisted.internet.defer import inlineCallbacks
from autobahn.twisted.util import sleep
import util

@inlineCallbacks
def main(session):
    try:
        # get list of provisioned nodes
        nodes = yield session.call(u'cdc.remote.list_nodes@1')

        for node_id in nodes:
            # get node status given node_id
            node_status = yield session.call(u'cdc.management.query_node@1',
                                             node_id)
            print('node "{}" is in status "{}"'.format(node_id, node_status))

        # our handler that will be called when a node changes status
        def on_node_status(node_id, old_status, new_status):
            print('node "{}"" changed state: "{}"" to "{}"'.format(node_id,
                                                                   old_status,
                                                                   new_status))

        yield session.subscribe(on_node_status,
                                u'cdc.remote.on_node_status@1')

        yield sleep(60)
    except:
        session.log.failure()

util.run(main)
