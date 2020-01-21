proc = 'com.example.add2'
args = [2, 3]
kwargs = None
options = None

def test():
    import requests, json
    payload = {'procedure': proc}
    if args:
        payload['args'] = list(args)
    if kwargs:
        payload['kwargs'] = dict(kwargs)
    headers = {'Content-Type': 'application/json'}
    r = requests.post('http://localhost:8080/call', data=json.dumps(payload), headers=headers)
    res = r.json()
    return res['args'][0]

print(test())
