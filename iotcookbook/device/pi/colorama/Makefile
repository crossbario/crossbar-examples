default:
	@echo "Targets: start, stop, restart, status, log, install"

start:
	sudo systemctl start colorama

stop:
	sudo systemctl stop colorama

restart:
	sudo systemctl restart colorama

status:
	systemctl status colorama

log:
	sudo journalctl -n 100 -f -u colorama

install:
	sudo cp colorama.service /etc/systemd/system/colorama.service
	sudo systemctl daemon-reload
	sudo systemctl enable colorama
	sudo systemctl restart colorama
