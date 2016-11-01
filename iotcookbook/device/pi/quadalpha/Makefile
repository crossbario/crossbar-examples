default:
	@echo "Targets: start, stop, restart, status, log, install"

start:
	sudo systemctl start votes

stop:
	sudo systemctl stop votes

restart:
	sudo systemctl restart votes

status:
	systemctl status votes

log:
	sudo journalctl -n 100 -f -u votes

install:
	sudo cp votes.service /etc/systemd/system/votes.service
	sudo systemctl daemon-reload
	sudo systemctl enable votes
	sudo systemctl restart votes
