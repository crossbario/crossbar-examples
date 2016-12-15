callee_only:
	/opt/crossbar/bin/crossbar start --config=config_callee_only.json

# test Crossbar.io/PyPy on Docker/armhf, using UDS-RawSocket-CBOR transport
test_pypy_fastest_rpc:
	sudo docker run --rm -it --user root -v `pwd`:/node crossbario/crossbar-armhf:community-pypy "--config=config_uds_rawsocket_cbor.json"

# test Crossbar.io/PyPy on Docker/armhf, using TCP-WebSocket-JSON transport
test_pypy_slowest_rpc:
	sudo docker run --rm -it --user root -v `pwd`:/node crossbario/crossbar-armhf:community-pypy "--config=config_tcp_websocket_json.json"

# test Crossbar.io/CPy on Docker/armhf, using UDS-RawSocket-CBOR transport
test_cpy_fastest_rpc:
	sudo docker run --rm -it --user root -v `pwd`:/node crossbario/crossbar-armhf:community "--config=config_uds_rawsocket_cbor.json"

# test Crossbar.io/CPy on Docker/armhf, using TCP-WebSocket-JSON transport
test_cpy_slowest_rpc:
	sudo docker run --rm -it --user root -v `pwd`:/node crossbario/crossbar-armhf:community "--config=config_tcp_websocket_json.json"
