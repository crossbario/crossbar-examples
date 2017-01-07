from twisted.internet.defer import inlineCallbacks
import util

@inlineCallbacks
def main(session):
    try:
        status = yield session.call(u'cdc.remote.status@1')
    except:
        session.log.failure()
    else:
        realm = status[u'realm']
        now = status[u'now']
        print('Connected to CDC realm "{}", time is {}'.format(realm, now))

util.run(main)
