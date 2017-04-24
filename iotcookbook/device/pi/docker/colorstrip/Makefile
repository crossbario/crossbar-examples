.PHONY: start

start:
	docker run -v ${PWD}/app:/app  -it --rm --link crossbar crossbario/autobahn-python-armhf

setup:
	sudo sh -c 'echo "blacklist snd_bcm2835" > /etc/modprobe.d/snd-blacklist.conf'
