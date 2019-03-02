test:
	-rm -rf ./results
	crossbarfx edge start --cbdir=./.crossbar --shutdownafter 120 --config=config_uds_rawsocket_cbor.json
	python analyze.py

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


# test Crossbar.io/PyPy on Docker/armhf, using UDS-RawSocket-CBOR transport
test_2x_pypy_fastest_rpc:
	sudo docker run --rm -it --user root -v `pwd`:/node crossbario/crossbar-armhf:community-pypy "--config=config_2x_uds_rawsocket_cbor.json"

# test Crossbar.io/CPy on Docker/armhf, using UDS-RawSocket-CBOR transport
test_2x_cpy_fastest_rpc:
	sudo docker run --rm -it --user root -v `pwd`:/node crossbario/crossbar-armhf:community "--config=config_2x_uds_rawsocket_cbor.json"
