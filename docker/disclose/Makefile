.PHONY: crossbar client docker

crossbar:
	sudo docker run \
		-v ${PWD}/crossbar:/node \
		-u 1000 \
		-p 8080:8080 \
		--name crossbar \
		--rm -it crossbario/crossbar

client:
	sudo docker run \
		-v ${PWD}/client:/root --link crossbar \
		--rm -it crossbario/autobahn-python:cpy3-alpine \
		python /root/client.py --url ws://crossbar:8080/ws --realm realm1

clean:
	-rm -f crossbar/.crossbar/key.*
	-rm -rf crossbar/__pycache__/

docker: clean
	sudo docker build -t myimage -f Dockerfile .

docker-test:
	sudo docker run --rm -it -p 8080:8080 myimage

docker-shell:
	sudo docker run --rm -it -p 8080:8080 --entrypoint /bin/sh myimage

