from zlmdb import MapStringCbor, table


class WampStatsRecord(object):
    def __init__(self):
        self.key = None
        self.calls_per_sec = None
        self.count = None
        self.avg_rtt = None
        self.max_rtt = None
        self.q50_rtt = None
        self.q99_rtt = None
        self.q995_rtt = None

    def marshal(self):
        obj = {
            'key': self.key,
            'calls_per_sec': self.calls_per_sec,
            'count': self.count,
            'avg_rtt': self.avg_rtt,
            'max_rtt': self.max_rtt,
            'q50_rtt': self.q50_rtt,
            'q99_rtt': self.q99_rtt,
            'q995_rtt': self.q995_rtt,
        }
        return obj

    @staticmethod
    def unmarshal(data):
        assert type(data) == dict

        obj = WampStatsRecord()

        if 'key' in data:
            assert type(data['key']) == str
            obj.key = data['key']

        if 'calls_per_sec' in data:
            assert type(data['calls_per_sec']) == int
            obj.calls_per_sec = data['calls_per_sec']

        if 'count' in data:
            assert type(data['count']) == int
            obj.count = data['count']

        if 'avg_rtt' in data:
            assert type(data['avg_rtt']) == float
            obj.avg_rtt = data['avg_rtt']

        if 'max_rtt' in data:
            assert type(data['max_rtt']) == float
            obj.max_rtt = data['max_rtt']

        if 'q50_rtt' in data:
            assert type(data['q50_rtt']) == float
            obj.q50_rtt = data['q50_rtt']

        if 'q99_rtt' in data:
            assert type(data['q99_rtt']) == float
            obj.q99_rtt = data['q99_rtt']

        if 'q995_rtt' in data:
            assert type(data['q995_rtt']) == float
            obj.q995_rtt = data['q995_rtt']

        return obj


@table('2e640ff3-aa58-4c1b-a2b4-e656517b692f', marshal=WampStatsRecord.marshal, parse=WampStatsRecord.unmarshal)
class WampStats(MapStringCbor):
    pass


class ProcStatsRecord(object):
    def __init__(self):
        self.key = None
        self.cpu = None
        self.mem = None
        self.ctx = None

    def marshal(self):
        obj = {
            'key': self.key,
            'cpu': self.cpu,
            'mem': self.mem,
            'ctx': self.ctx,
        }
        return obj

    @staticmethod
    def unmarshal(data):
        assert type(data) == dict

        obj = WampStatsRecord()

        if 'key' in data:
            assert type(data['key']) == str
            obj.key = data['key']

        if 'cpu' in data:
            assert type(data['cpu']) == float
            obj.cpu = data['cpu']

        if 'mem' in data:
            assert type(data['mem']) == float
            obj.mem = data['mem']

        if 'ctx' in data:
            assert type(data['ctx']) == int
            obj.ctx = data['ctx']

        return obj


@table('cd5bddf3-1fd3-4a70-9a74-205fc748c8a8', marshal=ProcStatsRecord.marshal, parse=ProcStatsRecord.unmarshal)
class ProcStats(MapStringCbor):
    pass


class Schema(object):

    proc_stats = None
    wamp_stats = None

    def __init__(self, db):
        self.db = db

    @staticmethod
    def attach(db):
        schema = Schema(db)
        schema.proc_stats = db.attach_table(ProcStats)
        schema.wamp_stats = db.attach_table(WampStats)

        return schema
