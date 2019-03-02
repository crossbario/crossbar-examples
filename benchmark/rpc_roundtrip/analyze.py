import argparse
import six
from pprint import pprint

from zlmdb import Database
from stats import Schema
import iso8601


if __name__ == '__main__':

    parser = argparse.ArgumentParser()

    parser.add_argument("--router", type=six.text_type, default=u"ws://10.1.1.11:9000", help='WAMP router URL.')
    parser.add_argument("--realm", type=six.text_type, default=u"realm1", help='WAMP router realm.')

    args = parser.parse_args()

    db = Database(dbpath='./results')
    schema = Schema.attach(db)

    with db.begin() as txn:
        cnt = schema.wamp_stats.count(txn)
        print(cnt)

        res = {}
        for rec_id, rec in schema.wamp_stats.select(txn):
            if True or rec_id.endswith('#caller.1.0'):
                ts, client = rec_id.split('#')
                ts = iso8601.parse_date(ts)
                client_type, instance, loop = client.split('.')
                instance = int(instance)
                loop = int(loop)
                if instance not in res:
                    res[instance] = {}
                if loop not in res[instance]:
                    res[instance][loop] = []
                res[instance][loop].append(rec.calls_per_sec)

        final = {}
        for instance in res:
            final[instance] = {}
            for loop in res[instance]:
                l = res[instance][loop]
                final[instance][loop] = int(round(sum(l) / len(l), 0))

                #print(ts, client_type, instance, loop, rec.marshal())

    pprint(final)