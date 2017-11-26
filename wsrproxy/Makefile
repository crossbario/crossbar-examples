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
