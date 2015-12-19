start:
	env NODE_PATH=${HOME}/scm/crossbario/crossbarexamples/demos/_demo_launcher/web/node_modules crossbar start --config config_prod.json

stop:
	crossbar stop

cert:
	letsencrypt certonly --webroot -w ./letsencrypt/ -d cbdemo-us-west-1.crossbar.io -d demo.crossbar.io
