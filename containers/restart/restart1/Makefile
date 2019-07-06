default:
	@echo "targets: all websocket rawsocket"

all: websocket rawsocket

# 2019-07-06T15:23:00+0200 [Container   18646] Encountered error at n=4096
# 2019-07-06T15:23:01+0200 [Container   18646] MySession.echo(): echo return 32 bytes
# 2019-07-06T15:23:01+0200 [Container   18646] Ok, session still working - leaving now ..
rawsocket:
	# OK! : Encountered error at n=8192 - autobahn.exception.PayloadExceededError
	-crossbar start --config config-rawsocket-1.json

	# ~OK : Encountered error at n=4096 - ApplicationError(error=<wamp.error.invalid_argument>)
	-crossbar start --config config-rawsocket-2.json

	# OK! : Encountered error at n=4096 - autobahn.exception.PayloadExceededError
	-crossbar start --config config-rawsocket-3.json

websocket:
	# OK! : Encountered error at n=8192 - autobahn.exception.PayloadExceededError
	-crossbar start --config config-websocket-1.json

	# OK! : Encountered error at n=4096 - autobahn.exception.PayloadExceededError
	-crossbar start --config config-websocket-2.json

	# FIXME: Encountered error at n=4096 - ApplicationError(error=<wamp.close.transport_lost>)
	-crossbar start --config config-websocket-3.json

router_rawsocket:
	# OK! : Finished (without error) at n=67108864
	-crossbar start --config config-router.json

	# OK! : Encountered error at n=8192 - ApplicationError(error=<wamp.error.invalid_argument>)
	-crossbar start --config config-router-rawsocket-1.json

	# OK! : Encountered error at n=8192 - autobahn.exception.PayloadExceededError
	-crossbar start --config config-router-rawsocket-2.json

	# OK! : Encountered error at n=8192 - ApplicationError(error=<wamp.error.invalid_argument>)
	-crossbar start --config config-router-websocket-1.json

	# OK! : Encountered error at n=8192 - autobahn.exception.PayloadExceededError
	-crossbar start --config config-router-websocket-2.json
