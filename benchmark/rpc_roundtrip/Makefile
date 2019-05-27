clean:
	-rm -rf ./results

test_uds_rawsocket_cbor:
	crossbarfx edge start --cbdir=./.crossbar --shutdownafter 120 --config=config_uds_rawsocket_cbor.json

test_tcp_websocket_cbor:
	crossbarfx edge start --cbdir=./.crossbar --shutdownafter 120 --config=config_tcp_websocket_cbor.json

test: test_uds_rawsocket_cbor test_tcp_websocket_cbor

analyze:
	python analyze.py
