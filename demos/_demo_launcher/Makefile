help:
	@echo ""
	@echo "Targets:"
	@echo ""
	@echo "     deploy       : Deploy updated Crossbar.io config and/or systemd service unit."
	@echo "     diff         : Diff between currently deployed Crossbar.io config / system service unit and Git"
	@echo "     update       : Update Crossbar.io installation (and restart the service)"
	@echo "     restart      : Restart Crossbar.io service"
	@echo "     status       : Get Crossbar.io service status"
	@echo "     log          : Live tail of the Crossbar.io service log"
	@echo "     test         : Manually start Crossbar.io (outside systemd, but under 'crossbar' service user"
	@echo ""

deploy:
	sudo systemctl stop crossbar
	sudo cp crossbar.service /etc/systemd/system/crossbar.service
	sudo systemctl daemon-reload
	sudo systemctl start crossbar

diff:
	diff crossbar.service /etc/systemd/system/crossbar.service

update:
	/home/ubuntu/cpy351_1/bin/pip install -U crossbar
	sed -i'' 's/python3.5/python3.5 -u/' /home/ubuntu/cpy351_1/bin/crossbar
	sudo setcap cap_net_bind_service=+ep /home/ubuntu/cpy351_1/bin/python3.5
	sudo setcap cap_net_bind_service=+ep /home/ubuntu/cpy351_1/bin/crossbar

restart:
	sudo systemctl restart crossbar

status:
	systemctl status crossbar

log:
	journalctl -f -n 120 -u crossbar

test:
	sudo -u crossbar /home/ubuntu/cpy351_1/bin/crossbar start --cbdir=/home/ubuntu/crossbarexamples/demos/_demo_launcher/.crossbar
