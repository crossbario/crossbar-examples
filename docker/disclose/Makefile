.PHONY: crossbar crossbar_dev client client_dev

REPOS=../..

crossbar:
	# FIXME: the Docker image runs Crossbar.io under user "daemon" - make sure it can write
	sudo chown -R daemon:daemon ./crossbar/.crossbar
	sudo docker run \
		-v ${PWD}/crossbar:/var/crossbar \
		-p 8080:8080 \
		--name crossbar \
		--rm -it crossbario/crossbar

crossbar_dev:
	sudo chown -R ${USER}:${USER} ./crossbar/.crossbar
	PYTHONPATH=$(REPOS)/autobahn:$(REPOS)/crossbar python -m crossbar.controller.cli start \
		--cbdir=./crossbar/.crossbar

client:
	sudo docker run \
		-v ${PWD}/client:/root --link crossbar \
		--rm -it crossbario/autobahn-python:cpy3-alpine \
		python /root/client.py --url ws://crossbar:8080/ws --realm realm1

client_dev:
	PYTHONPATH=$(REPOS)/autobahn-python python client/client.py \
		--url ws://localhost:8080/ws --realm realm1
