.PHONY: all monitor store notebook

all:
	@echo "Targets: monitor, store, notebook"

monitor:
	python monitor.py --port=/dev/ttyACM3 --router=wss://demo.crossbar.io/ws --realm=crossbardemo

store:
	python store.py --router=wss://demo.crossbar.io/ws --realm=crossbardemo

notebook:
	ipython notebook --notebook-dir=notebooks
