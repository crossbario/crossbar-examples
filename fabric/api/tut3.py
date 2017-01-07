from twisted.internet.defer import inlineCallbacks
import util

@inlineCallbacks
def main(session):
    try:
        # get all nodes in state "online"
        node_ids = yield session.call(u'cdc.remote.list_nodes@1')

        for node_id in node_ids:

            # get node status given node_id
            node_status = yield session.call(u'cdc.remote.query_node@1',
                                             node_id)

            if node_status['status'] == u'online':
                # get workers for each node
                worker_ids = yield session.call(u'cdc.remote.list_workers@1',
                                                node_id)

                for worker_id in worker_ids:
                    # query each worker found ..
                    worker = yield session.call(u'cdc.remote.query_worker@1',
                                                node_id, worker_id)

                    worker_type = worker[u'type']
                    print('worker "{}"-"{}": "{}"'.format(node_id,
                                                          worker_id,
                                                          worker_type))
    except:
        session.log.failure()

util.run(main)
