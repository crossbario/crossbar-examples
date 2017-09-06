update:
	docker pull crossbario/crossbar-fabric:latest

build:
	docker build -t crossbar-demos -f Dockerfile .

start_cf_interactive:
	docker run \
		--rm \
		--net=host \
		-p 80:80 \
		-p 443:443 \
		-v ${PWD}:/node \
		--entrypoint /usr/local/bin/crossbar \
		crossbar-demos \
			start --personality fabric --cbdir /node/.crossbar


start_cf:
	docker run \
		--detach \
		--restart always \
		--net=host \
		-p 443:443 \
		-v ${PWD}:/node \
		--name cf-node \
		--entrypoint /usr/local/bin/crossbar \
		crossbar-demos \
			start --personality fabric --cbdir /node/.crossbar
