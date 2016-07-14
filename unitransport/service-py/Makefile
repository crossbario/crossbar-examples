default: test

image:
	time sudo docker build -t unitransport-service-py -f Dockerfile .

test: image
	sudo docker run --rm -it -p 8080:8080 --name service-py --net=host unitransport-service-py

shell: image
	sudo docker run --rm -it -p 8080:8080 --name service-py --entrypoint /bin/sh --net=host unitransport-service-py

list:
	sudo docker images

clean:
	cd app && scons -uc
	sudo docker rmi unitransport-service-py
