from jsonschema import validate
from pprint import pprint


schema = {
    "type" : "object",
    "properties" : {
        "price" : {"type" : "number"},
        "name" : {"type" : "string"},
    },
}

validate({"name" : "Eggs", "price" : 34.99}, schema)
#validate({"name" : "Eggs", "price" : "Invalid"}, schema)

import json

with open('api.json') as f:
    schema = json.loads(f.read())
    pprint(schema)
