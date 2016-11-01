default:
	@echo "Targets: start, stop, restart, status, log, install"

start:
	sudo systemctl start gpio

stop:
	sudo systemctl stop gpio

restart:
	sudo systemctl restart gpio

status:
	systemctl status gpio

log:
	sudo journalctl -n 100 -f -u gpio

install:
	sudo cp gpio.service /etc/systemd/system/gpio.service
	sudo systemctl daemon-reload
	sudo systemctl enable gpio
	sudo systemctl restart gpio
