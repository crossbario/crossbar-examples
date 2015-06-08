proc = 'com.example.add2'
args = None
kwargs = None
options = None

def test():
    import requests, json
    print("foobar")
    payload = {"procedure": proc}
    if args:
        payload['args'] = list(args)
    if kwargs:
        payload['kwargs'] = dict(kwargs)
    headers = {'Content-Type': 'application/json'}
    r = requests.post("http://127.0.0.1:8080/call", data=json.dumps(payload), headers=headers)
    return r.text
    res = r.json()
    return res['args'][0]

test()
