.PHONY: crossbar client

HOSTIP=$(shell ip route get 1 | awk '{print $$NF;exit}')

crossbar:
	# FIXME: the Docker image runs Crossbar.io under user "daemon" - make sure it can write
	chmod 777 ./crossbar/.crossbar
	sudo docker run -v ${PWD}/crossbar:/var/crossbar \
		-p 8080:8080 \
		-it crossbario/crossbar

client:
	sudo docker run -v ${PWD}/client:/root \
		-it crossbario/autobahn-python:cpy3-alpine \
		python /root/client.py --url ws://$(HOSTIP):8080/ws --realm realm1
