# Dashboard Demo

Graphical, real-time dashboard.

## Frontend

All the HTML5 assets for the frontend reside in this folder. You can start the demo by opening the `index.html` in your browser.

## Backend

The backend for this demo consists of a `sales` table equipped with PL/SQL triggers that compute aggregate data and publish WAMP events.

There is a fake sales event generator that issues SQL `INSERT` statements against the `sales` table. 

You can start the fake generator by doing

	python python/salesdriver.py --host=192.168.56.102

providing the hostname or IP address for your Oracle instance. For other options run the `salesdriver.py` with `--help`.
