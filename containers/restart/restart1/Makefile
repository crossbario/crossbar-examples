default:
	@echo "targets: all websocket rawsocket"

all: rpc pubsub

rpc: rpc_rawsocket rpc_websocket rpc_router

pubsub: pubsub_rawsocket pubsub_websocket pubsub_router

# 2019-07-06T15:23:00+0200 [Container   18646] Encountered error at n=4096
# 2019-07-06T15:23:01+0200 [Container   18646] MySession.echo(): echo return 32 bytes
# 2019-07-06T15:23:01+0200 [Container   18646] Ok, session still working - leaving now ..
rpc_rawsocket:
	# OK! : Encountered error at n=8192 - autobahn.exception.PayloadExceededError
	-crossbar start --config config-rpc-rawsocket-1.json

	# ~OK : Encountered error at n=4096 - ApplicationError(error=<wamp.error.invalid_argument>)
	-crossbar start --config config-rpc-rawsocket-2.json

	# OK! : Encountered error at n=4096 - autobahn.exception.PayloadExceededError
	-crossbar start --config config-rpc-rawsocket-3.json

rpc_websocket:
	# OK! : Encountered error at n=8192 - autobahn.exception.PayloadExceededError
	-crossbar start --config config-rpc-websocket-1.json

	# OK! : Encountered error at n=4096 - autobahn.exception.PayloadExceededError
	-crossbar start --config config-rpc-websocket-2.json

	# WebSocket does not have max_message_length negotiation (as does RawSocket)!!!
	# Because of that, the max_message_length for client and router must be
	# configured _identical_ - otherwise (eg if one is smaller than the other), the peer
	# with the smaller max_msg_size will be sent a "too large" message (as it is not caught
	# in Autobahn _before_ sending on the wire)
	# OK!: Encountered error at n=8192 - ApplicationError(error=<wamp.close.transport_lost>)
	-crossbar start --config config-rpc-websocket-3.json

rpc_router:
	# OK! : Finished (without error) at n=67108864
	-crossbar start --config config-rpc-router.json

	# OK! : Encountered error at n=8192 - ApplicationError(error=<wamp.error.invalid_argument>)
	-crossbar start --config config-rpc-router-rawsocket-1.json

	# OK! : Encountered error at n=8192 - autobahn.exception.PayloadExceededError
	-crossbar start --config config-rpc-router-rawsocket-2.json

	# OK! : Encountered error at n=8192 - ApplicationError(error=<wamp.error.invalid_argument>)
	-crossbar start --config config-rpc-router-websocket-1.json

	# OK! : Encountered error at n=8192 - autobahn.exception.PayloadExceededError
	-crossbar start --config config-rpc-router-websocket-2.json


pubsub_rawsocket:
	# OK! : Encountered error at n=16384 - autobahn.exception.PayloadExceededError
	-crossbar start --config config-pubsub-rawsocket-1.json

	# OK! : 1) could not dispatch event to receiver .. + 2) Encountered error at n=16384 - autobahn.exception.PayloadExceededError
	-crossbar start --config config-pubsub-rawsocket-2.json

	# OK! : Encountered error at n=8192 - autobahn.exception.PayloadExceededError
	-crossbar start --config config-pubsub-rawsocket-3.json

pubsub_websocket:
	# OK! : Encountered error at n=16384 - autobahn.exception.PayloadExceededError
	-crossbar start --config config-pubsub-websocket-1.json

	# OK! : Encountered error at n=16384 - autobahn.exception.PayloadExceededError
	-crossbar start --config config-pubsub-websocket-2.json

	# OK! : Encountered error at n=16384 - autobahn.exception.PayloadExceededError
	-crossbar start --config config-pubsub-websocket-3.json

pubsub_router:
	# OK! : Finished (without error) at n=67108864
	-crossbar start --config config-pubsub-router.json

	# OK! : Encountered error at n=16384 - autobahn.exception.PayloadExceededError
	-crossbar start --config config-pubsub-router-rawsocket-1.json

	# OK! : 1) could not dispatch event to receiver .. + 2) Finished (without error) at n=67108864
	-crossbar start --config config-pubsub-router-rawsocket-2.json

	# OK! : Encountered error at n=16384 - autobahn.exception.PayloadExceededError
	-crossbar start --config config-pubsub-router-websocket-1.json

	# OK! : 1) could not dispatch event to receiver .. + 2) Finished (without error) at n=67108864
	-crossbar start --config config-pubsub-router-websocket-2.json
