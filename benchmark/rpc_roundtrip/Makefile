callee_only:
	/opt/crossbar/bin/crossbar start --config=config_callee_only.json

# test Crossbar.io/PyPy on Docker/armhf, using UDS-RawSocket-CBOR transport
test_fastest_ipc:
	sudo docker run --rm -it --user root -v `pwd`:/node crossbario/crossbar-armhf:community-pypy "--config=config_uds_rawsocket_cbor.json"

# test Crossbar.io/PyPy on Docker/armhf, using TPC-WebSocket-JSON transport
test_slowest_ipc:
	sudo docker run --rm -it --user root -v `pwd`:/node crossbario/crossbar-armhf:community-pypy "--config=config_tcp_websocket_json.json"
