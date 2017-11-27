crossbar:
	crossbar start --personality=community

server1:
	python server.py --endpoint=tcp:9000 --url=ws://localhost:9000

server2:
	python server.py --endpoint=tcp:9001 --url=ws://localhost:9001

client1:
	python client.py --url=ws://localhost:8080/proxy1

client2:
	python client.py --url=ws://localhost:8080/proxy2

client3:
	python wamp_client.py \
		--endpoint=tcp:host=127.0.0.1:port=9002 \
		--url=ws://localhost:9002 \
		--realm=realm1

client4:
	python wamp_client.py \
		--endpoint=tcp:host=127.0.0.1:port=8080 \
		--url=ws://localhost:8080/proxy3 \
		--realm=realm1
