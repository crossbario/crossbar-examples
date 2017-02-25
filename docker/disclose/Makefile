.PHONY: crossbar client

REPOS=../..

crossbar:
	sudo docker run \
		-v ${PWD}/crossbar:/var/crossbar \
		-p 8080:8080 \
		--name crossbar \
		--rm -it crossbario/crossbar

client:
	sudo docker run \
		-v ${PWD}/client:/root --link crossbar \
		--rm -it crossbario/autobahn-python:cpy3-alpine \
		python /root/client.py --url ws://crossbar:8080/ws --realm realm1
