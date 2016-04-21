proc = u'com.example.add2'
args = [2, 3]
kwargs = None
options = None

def test():
    import requests, json
    payload = {u'procedure': proc}
    if args:
        payload[u'args'] = list(args)
    if kwargs:
        payload[u'kwargs'] = dict(kwargs)
    headers = {u'Content-Type': u'application/json'}
    r = requests.post(u'http://localhost:8080/call', data=json.dumps(payload), headers=headers)
    res = r.json()
    return res[u'args'][0]

print(test())
