import argparse
from pprint import pprint

from zlmdb import Database
from stats import Schema
import iso8601


if __name__ == '__main__':

    parser = argparse.ArgumentParser()

    parser.add_argument("--router", type=str, default="ws://10.1.1.11:9000", help='WAMP router URL.')
    parser.add_argument("--realm", type=str, default="realm1", help='WAMP router realm.')

    args = parser.parse_args()

    db = Database(dbpath='./results')
    schema = Schema.attach(db)

    with db.begin() as txn:
        cnt = schema.wamp_stats.count(txn)
        print(cnt)

        res = {}
        for (batch_id, ts), rec in schema.wamp_stats.select(txn):
            if rec.worker not in res:
                res[rec.worker] = {}
            if rec.loop not in res[rec.worker]:
                res[rec.worker][rec.loop] = []
            res[rec.worker][rec.loop].append(rec.calls_per_sec)

    final_avg = {}
    for instance in res:
        final_avg[instance] = {}
        for loop in res[instance]:
            l = res[instance][loop]
            final_avg[instance][loop] = int(round(sum(l) / len(l), 0))

    pprint(final_avg)

    final_total = 0
    for instance in final_avg:
        for loop in final_avg[instance]:
            final_total += final_avg[instance][loop]

    print(final_total)
