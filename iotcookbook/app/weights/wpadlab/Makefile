.PHONY: all monitor monitor_local store store_local crossbar_local notebook

all:
	@echo "Targets: monitor, monitor_local, store, store_local, crossbar_local, notebook"

monitor:
	python monitor.py --port=/dev/ttyACM3 --router=wss://demo.crossbar.io/ws --realm=crossbardemo

monitor_local:
	python monitor.py --port=/dev/ttyACM3 --router=ws://localhost:8080/ws --realm=iot_cookbook

store:
	python store.py --router=wss://demo.crossbar.io/ws --realm=crossbardemo

store_local:
	python store.py --router=ws://localhost:8080/ws --realm=iot_cookbook

crossbar_local:
	crossbar start

notebook:
	ipython notebook --notebook-dir=notebooks

clean:
	rm -f *.dat.*
	rm -rf notebooks/.ipynb_checkpoints
