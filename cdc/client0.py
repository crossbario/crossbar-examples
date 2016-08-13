from twisted.internet.defer import inlineCallbacks
import cdc

@inlineCallbacks
def main(session, details):
    try:
        now = yield session.call(u'com.crossbario.cdc.api.get_now')
    except:
        session.log.failure()
    else:
        session.log.info("Current time at CDC: {now}", now=now)

cdc.run(main, keyfile='mykey')
