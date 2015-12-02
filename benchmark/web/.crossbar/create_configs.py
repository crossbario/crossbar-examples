WORKER = u"""
{
    "type": "router",
    "options": {
       "cpu_affinity": [%(cpu_affinity)s],
       "pythonpath": [".."]
    },
    "transports": [
       {
          "type": "web",
          "endpoint": {
             "type": "tcp",
             "port": 8080,
             "backlog": 2048,
             "shared": true
          },
          "paths": {
             "/": {
                "type": "static",
                "directory": ".."
             },
             "resource": {
                "type": "resource",
                "classname": "myresource.MyResource"
             },
             "json": {
                "type": "json",
                "value": {
                   "param1": "foobar",
                   "param2": [1, 2, 3],
                   "param3": {
                      "awesome": true,
                      "nifty": "yes"
                   }
                }
             }
          }
       }
    ]
}
"""

import json

for num in [1, 2, 4, 8, 16, 32, 40, 48]:
    config = {'workers': []}
    for i in range(num):
        worker = WORKER % {'cpu_affinity': i}
        worker = json.loads(worker)
        config['workers'].append(worker)
    contents = json.dumps(config, sort_keys=True, indent=3, ensure_ascii=False)
    with open('config_w{}.json'.format(i + 1), 'w') as f:
        f.write(contents)
