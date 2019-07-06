default:
	@echo "targets: websocket rawsocket"

websocket:
	-crossbar start --config config-websocket-1.json
	-crossbar start --config config-websocket-2.json
	-crossbar start --config config-websocket-3.json

# 2019-07-06T15:23:00+0200 [Container   18646] Encountered error at n=4096
# 2019-07-06T15:23:01+0200 [Container   18646] MySession.echo(): echo return 32 bytes
# 2019-07-06T15:23:01+0200 [Container   18646] Ok, session still working - leaving now ..
rawsocket:
	-crossbar start --config config-rawsocket-1.json
	-crossbar start --config config-rawsocket-2.json
	-crossbar start --config config-rawsocket-3.json
