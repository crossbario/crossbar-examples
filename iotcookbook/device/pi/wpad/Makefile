default:
	@echo "Targets: start, stop, restart, status, log, install"

start:
	sudo systemctl start wpad

stop:
	sudo systemctl stop wpad

restart:
	sudo systemctl restart wpad

status:
	systemctl status wpad

log:
	sudo journalctl -n 100 -f -u wpad

requirements:
	sudo apt-get update
	sudo apt-get install -y build-essential python-dev git scons swig
	sudo pip install -U -r requirements.txt
	cd /tmp && \
	git clone https://github.com/jgarff/rpi_ws281x.git && \
	cd rpi_ws281x && \
	scons && \
	cd python && \
	sudo python setup.py install

	# disable audio, as this interferes with the Neopixel PCM trick
	# see: https://github.com/jgarff/rpi_ws281x#limitations
	sudo echo "blacklist snd_bcm2835" > /etc/modprobe.d/snd-blacklist.conf

install:
	sudo cp wpad.service /etc/systemd/system/wpad.service
	sudo systemctl daemon-reload
	sudo systemctl enable wpad
	sudo systemctl restart wpad

test:
	sudo python -u wpad.py
