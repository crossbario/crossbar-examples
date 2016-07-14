default: test

image:
	time sudo docker build -t unitransport-service-cpp -f Dockerfile .

test: image
	sudo docker run --rm -it -p 8080:8080 --name service-cpp --net=host --entrypoint=/usr/local/app/client unitransport-service-cpp

shell: image
	sudo docker run --rm -it -p 8080:8080 --name service-cpp --entrypoint /bin/sh --net=host unitransport-service-cpp

list:
	sudo docker images

clean:
	cd app && scons -uc
	sudo docker rmi unitransport-service-cpp
