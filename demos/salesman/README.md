# TSP Scaling demo

Crunch the Traveling Salesman Problem using multiple compute nodes.

- install NodeJS dependencies by doing 'npm install' (required for the orchestrator component and any compute nodes you run in Node.js)
- run Crossbar by doing 'crossbar start'
- open at least one browser tab to 'localhost:8080' to get the control interface + to run a browser compute node
- open as many more tabs as you like. these connect to your instance automatically when on the same machine. Otherwiser - FIXME!

The backend orchestrator running under NodeJS creates a set of cities and then  calls compute components in batches. After each batch, the best route is determined and used when calling the next batch.

Watch log output to see stuff happening in the compute nodes.

--- more docs and compue nodes for Python and C++ coming soon ---
