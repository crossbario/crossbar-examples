test:
	docker run --rm -it \
		--user 1000 \
		-v ${PWD}/node:/node \
		-v ${PWD}/../../_shared-web-resources:/node/_shared-web-resources \
		-p 8080:8080 \
		--name crossbar \
		crossbario/crossbar
