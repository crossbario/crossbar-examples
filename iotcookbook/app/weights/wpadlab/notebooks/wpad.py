# Define a helper function to call into Wpad procedures via the Crossbar.io REST bridge

#rpc_url = "https://demo.crossbar.io/call"
rpc_url = "http://localhost:8080/call"

import requests, json

def call(proc, *args, **kwargs):
    payload = {
        "procedure": proc,
        "args": args,
        "kwargs": kwargs
    }
    r = requests.post(rpc_url, data=json.dumps(payload),
                      headers={'content-type': 'application/json'})
    res = r.json()
    return res['args'][0]
