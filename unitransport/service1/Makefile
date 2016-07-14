default: test

image:
	time sudo docker build -t unitransport-service1 -f Dockerfile .

test: image
	sudo docker run --rm -it -p 8080:8080 --name service1 --net=host unitransport-service1

shell: image
	sudo docker run --rm -it -p 8080:8080 --name service1 --entrypoint /bin/sh --net=host unitransport-service1

list:
	sudo docker images

clean:
	cd app && scons -uc
	sudo docker rmi unitransport-service1
