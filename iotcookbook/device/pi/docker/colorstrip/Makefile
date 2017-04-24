.PHONY: start

start:
	docker run -it --rm \
		--device /dev/ttyAMA0 \
		--device /dev/mem \
		--device /dev/gpiomem \
		--privileged \
		--net=host \
		-v ${PWD}/app:/app \
		-e CBURL='wss://demo.crossbar.io/ws' \
		-e CBREALM='crossbardemo' \
		crossbario/autobahn-python-armhf

build:
	docker build -t iotcookbook-colostrip -f Dockerfile .

setup:
	sudo sh -c 'echo "blacklist snd_bcm2835" > /etc/modprobe.d/snd-blacklist.conf'
