default: test

image:
	time sudo docker build -t unitransport-service-js -f Dockerfile .

test: image
	sudo docker run --rm -it -p 8080:8080 --name service-js --net=host unitransport-service-js

shell: image
	sudo docker run --rm -it -p 8080:8080 --name service-js --entrypoint /bin/sh --net=host unitransport-service-js

list:
	sudo docker images

clean:
	cd app && scons -uc
	sudo docker rmi unitransport-service-js
