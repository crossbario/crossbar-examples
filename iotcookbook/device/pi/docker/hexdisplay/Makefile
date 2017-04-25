.PHONY: start

build:
	docker build -t cookbook-hexdisplay -f Dockerfile .

start: build
	docker run -it --rm \
		--device /dev/ttyAMA0 \
		--device /dev/mem \
		--device /dev/gpiomem \
		--privileged \
		--net=host \
		-e CBURL='wss://demo.crossbar.io/ws' \
		-e CBREALM='crossbardemo' \
		cookbook-hexdisplay

bash: build
	docker run -it --rm \
		--device /dev/ttyAMA0 \
		--device /dev/mem \
		--device /dev/gpiomem \
		--privileged \
		--net=host \
		-e CBURL='wss://demo.crossbar.io/ws' \
		-e CBREALM='crossbardemo' \
		cookbook-hexdisplay \
		/bin/bash
