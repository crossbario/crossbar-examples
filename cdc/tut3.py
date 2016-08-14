from twisted.internet.defer import inlineCallbacks
from autobahn.twisted.util import sleep
import util

NODE_ID = u'node0'
WORKER_ID = u'worker-002'

@inlineCallbacks
def main(session, details):
    try:
        log_topic = u'com.crossbario.cdc.node.{}.worker.{}.on_log'.format(NODE_ID, WORKER_ID)

        def on_worker_log(*args, **kwargs):
            print(args, kwargs)

        sub = yield session.subscribe(on_worker_log, log_topic)

        # com.crossbario.cdc.node.node0.get_worker_log
        log = yield session.call(u'com.crossbario.cdc.node.node0.get_worker_log', WORKER_ID, 30)

        #log = yield session.call(u'com.crossbario.cdc.remote.get_worker_log@1', NODE_ID, WORKER_ID, 30)
        for log_rec in log:
            print(log_rec)
    except:
        session.log.failure()
    else:
        yield sleep(10)

util.run(main)
