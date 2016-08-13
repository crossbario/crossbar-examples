from twisted.internet.defer import inlineCallbacks
import util

@inlineCallbacks
def main(session, details):
    try:
        status = yield session.call(u'com.crossbario.cdc.general.get_status@1')
    except:
        session.log.failure()
    else:
        session.log.info('Connected to CDC management realm "{realm}" (current time at CDC is {now})',
                         realm=status[u'realm'], now=status[u'now'])

util.run(main)
