# update CF image
update:
	docker pull crossbario/crossbar-fabric:latest

# start cbdemo node from CF image - interactively
start_cf_interactive:
	docker run \
		--rm \
		--net=host \
		-p 80:80 \
		-p 443:443 \
		-v ${PWD}/..:/node \
		--entrypoint /usr/local/bin/crossbar \
		crossbario/crossbar-fabric:latest \
			start --personality fabric --cbdir /node/_demo_launcher/.crossbar

# start cbdemo node from CF image - daemonized
start_cf:
	docker run \
		--detach \
		--restart always \
		--net=host \
		-p 80:80 \
		-p 443:443 \
		-v ${PWD}/..:/node \
		--name cbdemo \
		--entrypoint /usr/local/bin/crossbar \
		crossbario/crossbar-fabric:latest \
			start --personality fabric --cbdir /node/_demo_launcher/.crossbar
