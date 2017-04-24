.PHONY: start

build:
	docker build -t cookbook-colorstrip -f Dockerfile .

start: build
	docker run -it --rm \
		--device /dev/ttyAMA0 \
		--device /dev/mem \
		--device /dev/gpiomem \
		--privileged \
		--net=host \
		-e CBURL='wss://demo.crossbar.io/ws' \
		-e CBREALM='crossbardemo' \
		cookbook-colorstrip

prepare:
	sudo sh -c 'echo "blacklist snd_bcm2835" > /etc/modprobe.d/snd-blacklist.conf'
