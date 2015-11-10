# wrk -c 128 -t 8 --latency -d 60 http://10.0.1.3:8080/json

from pprint import pprint

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages


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
                data['reqs_per_sec'] = val
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
    'result_w8_3.log': 8
}

TESTS = {
    "wrk -c 128 -t 8 --latency -d 60 http://10.0.1.3:8080/": "txweb",
    "wrk -c 128 -t 8 --latency -d 60 http://10.0.1.3:8080/json": "json",
    "wrk -c 128 -t 8 --latency -d 60 http://10.0.1.3:8080/resource?count=256": "reply256",
    "wrk -c 128 -t 8 --latency -d 60 http://10.0.1.3:8080/resource?count=4096": "reply4096",
    "wrk -c 128 -t 8 --latency -d 60 http://10.0.1.3:8080/resource?count=65536": "reply65536",
}

def process2():
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
    pprint(res_p)

    print('test,workers,reqs_per_sec,mbyte_per_sec')
    for t in sorted(res_p):
        for f in sorted(res_p[t]):
            data = res_p[t][f]
            print('{},{},{},{}'.format(TESTS[t], FILES[f], int(round(data['req_per_sec'])), int(round(data['mbyte_per_sec']))))


def process():
    res = {}
    for f in sorted(FILES):
        workers = FILES[f]
        d = extract(f)
        for t in sorted(d):
            test = TESTS[t]
            if test not in res:
                res[test] = {
                    'reqs_per_sec': [],
                    'mbyte_per_sec': []
                }
            res[test]['reqs_per_sec'].append(d[t]['reqs_per_sec'])
            res[test]['mbyte_per_sec'].append(d[t]['mbyte_per_sec'])
    return res


def bar(ax, data, title, y_title):
    title = ax.set_title(title)
    title.set_position([.5, 1.2])
    #ax.set_xlabel('number of workers')
    ax.set_ylabel(y_title)

    width = .6
    ind = np.arange(len(data))

    ax.set_xticks(ind + .5)
    ax.set_xticklabels(('1', '2', '4', '8'))
    ax.bar(ind + .2, data, width, color='y')


def test():
    pdf = PdfPages("results.pdf")

    fig_width_cm = 21                         # A4 page
    fig_height_cm = 29.7
    inches_per_cm = 1 / 2.54              # Convert cm to inches
    fig_width = fig_width_cm * inches_per_cm # width in inches
    fig_height = fig_height_cm * inches_per_cm       # height in inches
    fig_size = [fig_width, fig_height]


    fig, axarr = plt.subplots(4, 2)
    fig.set_size_inches(fig_size)
    fig.subplots_adjust(wspace=.4, hspace=.7)
    fig.suptitle("Crossbar.io multi-core scaling for Web services", fontsize=12)

    data = process()

    #pprint(data)

    bar(axarr[0][0], data['json']['reqs_per_sec'], "JSON value resource", "requests/sec")
    bar(axarr[0][1], data['json']['mbyte_per_sec'], "JSON value resource", "MB/sec")

    bar(axarr[1][0], data['reply256']['reqs_per_sec'], "Fixed resource (256 bytes reply)", "requests/sec")
    bar(axarr[1][1], data['reply256']['mbyte_per_sec'], "Fixed resource (256 bytes reply)", "MB/sec")

    bar(axarr[2][0], data['reply4096']['reqs_per_sec'], "Fixed resource (4096 bytes reply)", "requests/sec")
    bar(axarr[2][1], data['reply4096']['mbyte_per_sec'], "Fixed resource (4096 bytes reply)", "MB/sec")

    bar(axarr[3][0], data['reply65536']['reqs_per_sec'], "Fixed resource (65536 bytes reply)", "requests/sec")
    bar(axarr[3][1], data['reply65536']['mbyte_per_sec'], "Fixed resource (65536 bytes reply)", "MB/sec")

#    bar(axarr[4][0], data['txweb']['reqs_per_sec'], "Static file resource", "requests/sec")
#    bar(axarr[4][1], data['txweb']['mbyte_per_sec'], "Static file resource", "MB/sec")

    pdf.savefig()
    pdf.close()

    plt.clf()

#process()
test()
