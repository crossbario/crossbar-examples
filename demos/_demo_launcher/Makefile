# update CF image
update:
	docker pull crossbario/crossbar-fabric:latest
	docker stop cbdemo
	docker rm cbdemo

# start cbdemo node from CF image - interactively
start_cf_interactive:
	docker run \
		--rm \
		--net=host \
		-p 80:80 \
		-p 443:443 \
		-v ${HOME}/scm/crossbario:/crossbario \
		--entrypoint /usr/local/bin/crossbar \
		crossbario/crossbar-fabric:latest \
			start --personality fabric --cbdir /crossbario/crossbar-examples/demos/_demo_launcher/.crossbar

# start cbdemo node from CF image - daemonized
start_cf:
	docker run \
		--detach \
		--restart always \
		--net=host \
		-p 80:80 \
		-p 443:443 \
		-v ${HOME}/scm/crossbario:/crossbario \
		--name cbdemo \
		--entrypoint /usr/local/bin/crossbar \
		crossbario/crossbar-fabric:latest \
			start --personality fabric --cbdir /crossbario/crossbar-examples/demos/_demo_launcher/.crossbar
