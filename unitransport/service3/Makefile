default: test

image:
	time sudo docker build -t unitransport-service3 -f Dockerfile .

test: image
	sudo docker run --rm -it -p 8080:8080 --name service3 --net=host unitransport-service3

shell: image
	sudo docker run --rm -it -p 8080:8080 --name service3 --entrypoint /bin/sh --net=host unitransport-service3

list:
	sudo docker images

clean:
	cd app && scons -uc
	sudo docker rmi unitransport-service3
