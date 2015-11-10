# wrk -c 128 -t 8 --latency -d 60 http://10.0.1.3:8080/json

from pprint import pprint


def extract(filename):
    res = {}
    with open(filename) as fd:
        test = None
        data = {}
        for line in fd.read().splitlines():
            if line.startswith('wrk'):
                if test:
                    res[test] = data
                    data = {}
                test = line
            elif line.startswith('Requests/sec'):
                val = float(line.split()[1])
                data['req_per_sec'] = val
                #print(val)
            elif line.startswith('Transfer/sec'):
                s = line.split()[1]
                unit = s[-2:]
                val = float(s[:-2])
                assert(unit in ['GB', 'MB'])
                if unit == 'GB':
                    val = val * 1000
                data['mbyte_per_sec'] = val
                #print(val, unit)
        res[test] = data
    return res

FILES = {
    'result_w1_2.log': 1,
    'result_w2_2.log': 2,
    'result_w4_2.log': 4,
    'result_w8_3.log': 5
}

TESTS = {
    "wrk -c 128 -t 8 --latency -d 60 http://10.0.1.3:8080/": "txweb",
    "wrk -c 128 -t 8 --latency -d 60 http://10.0.1.3:8080/json": "json",
    "wrk -c 128 -t 8 --latency -d 60 http://10.0.1.3:8080/resource?count=256": "reply256",
    "wrk -c 128 -t 8 --latency -d 60 http://10.0.1.3:8080/resource?count=4096": "reply4096",
    "wrk -c 128 -t 8 --latency -d 60 http://10.0.1.3:8080/resource?count=65536": "reply65536",
}

res = {}
for f in FILES:
    res[f] = extract(f)
#pprint(res)

res_p = {}
for f in res:
    for t in res[f]:
        if t not in res_p:
            res_p[t] = {}
        #if f not in res_p[t]:
        #    res_p[t] = {}
        res_p[t][f] = res[f][t]
#pprint(res_p)

print('test,workers,reqs_per_sec,mbyte_per_sec')
for t in sorted(res_p):
    for f in sorted(res_p[t]):
        data = res_p[t][f]
        print('{},{},{},{}'.format(TESTS[t], FILES[f], int(round(data['req_per_sec'])), int(round(data['mbyte_per_sec']))))
