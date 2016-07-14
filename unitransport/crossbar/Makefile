test:
	crossbar start --cbdir=./node/.crossbar --config config.json

test_with_guest:
	crossbar start --cbdir=./node/.crossbar --config config-with-guests.json

docker:
	sudo rm -f ./node/.crossbar/node.key
	time sudo docker build -t cbdemo-crossbar1 -f Dockerfile .

test_docker:
	sudo docker run --rm -it -p 8080:8080 --name crossbar cbdemo-crossbar1

test_docker_sh:
	sudo docker run --rm -it -p 8080:8080 --name crossbar --entrypoint /bin/sh cbdemo-crossbar1

list:
	sudo docker images

clean:
	sudo docker rmi cbdemo-crossbar1
