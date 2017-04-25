.PHONY: mount login prepare build start

PI='pi@192.168.1.31'

prepare_host:
	sudo apt install -y vde2

mount:
	# https://blog.dhampir.no/content/reverse-sshfs-mounts-fs-push
	dpipe /usr/lib/openssh/sftp-server = ssh ${PI} sshfs :${PWD} /home/pi/colorstrip -o slave &

login:
	ssh ${PI}

prepare_pi:
	sudo sh -c 'echo "blacklist snd_bcm2835" > /etc/modprobe.d/snd-blacklist.conf'

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
