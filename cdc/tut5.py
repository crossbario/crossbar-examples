from twisted.internet.defer import inlineCallbacks
from autobahn.twisted.util import sleep
import util

node_id = u'node0'
worker_id = u'worker-002'

@inlineCallbacks
def main(session):
    try:
        # retrieve log history of worker
        log = yield session.call(u'cdc.remote.query_worker_log@1',
                                 node_id, worker_id, 30)

        for log_rec in log:
            print(log_rec)

        # subscribe to live log stream from worker
        def on_worker_log(*args, **kwargs):
            print(args, kwargs)

        log_topic = yield session.call(u'cdc.remote.map_worker_log_topic@1',
                                       node_id, worker_id, 30)

        sub = yield session.subscribe(on_worker_log, log_topic)
        print('Listening to live log output ..')
    except:
        session.log.failure()
    else:
        yield sleep(15)

util.run(main)
