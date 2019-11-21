crossbar:
	crossbar start

test: websocket rawsocket

websocket:
	python client.py --url ws://localhost:8080/ws
	python client.py --url ws://localhost:8080/ws --serializer cbor
	python client.py --url ws://localhost:8080/ws --serializer msgpack
	python client.py --url ws://localhost:8080/ws --serializer json

rawsocket:
	python client.py --url rs://localhost:8081
	python client.py --url rs://localhost:8081 --serializer cbor
	python client.py --url rs://localhost:8081 --serializer msgpack
	python client.py --url rs://localhost:8081 --serializer json
