# TSP Scaling demo

Crunch the Traveling Salesman Problem using multiple compute nodes.

- install NodeJS dependencies by doing 'npm install'
- run Crossbar by doing 'crossbar start'
- open at least one browser tab to 'localhost:8080'
- open as many more tabs as you like, on any machine which can reach your machione

The backend orchestrator running under NodeJS creates a set of cities and then  calls compute components in batches. After each batch, the best route is determined and used when calling the next batch.

Watch log output to see stuff happening.

--- more docs and compue nodes for Python and C++ coming soon --- 
