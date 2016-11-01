default:
	@echo "Targets: start, stop, restart, status, log, install"

start:
	sudo systemctl start dispenser

stop:
	sudo systemctl stop dispenser

restart:
	sudo systemctl restart dispenser

status:
	systemctl status dispenser

log:
	sudo journalctl -n 100 -f -u dispenser

install:
	sudo cp dispenser.service /etc/systemd/system/dispenser.service
	sudo systemctl daemon-reload
	sudo systemctl enable dispenser
	sudo systemctl restart dispenser
