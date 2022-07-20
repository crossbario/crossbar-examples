import os
from typing import Optional

from twisted.internet.defer import inlineCallbacks
from twisted.internet.task import LoopingCall

from txaio import time_ns

from autobahn import wamp
from autobahn.util import hltype, hlval, hlid
from autobahn.wamp.exception import ApplicationError
from autobahn.wamp.types import SessionDetails, CloseDetails, CallDetails, RegisterOptions, PublishOptions
from autobahn.twisted.wamp import ApplicationSession


class ExampleBackend(ApplicationSession):

    def __init__(self, config):
        super().__init__(config)
        self._counter = 0
        self._periodic_loop = LoopingCall(self._periodic)

    @inlineCallbacks
    def onJoin(self, details: SessionDetails):
        self.log.info('{func} session joined with details {details}', func=hltype(self.onJoin), details=details)

        regs = yield self.register(self)
        for reg in regs:
            self.log.info('{func} registered procedure "{proc}"', func=hltype(self.onJoin), proc=hlid(reg.procedure))

        period = 10.
        self._periodic_loop.start(period, now=False)
        self.log.info('{func} started background loop ({period}s period)', func=hltype(self.onOpen),
                      period=hlval(period))

        self.log.info('{func} ready!', func=hltype(self.onJoin))

    def onLeave(self, details: CloseDetails):
        self.log.info('{func} details={details}', func=hltype(self.onLeave), details=details)

    @inlineCallbacks
    def _periodic(self):
        self._counter += 1

        topic = 'com.example.private.' \
                'replica.ba3b1e9f-3006-4eae-ae88-cf5896b36342.' \
                'clock.ba3b1e9f-3006-4eae-ae88-cf5896b36342.on_clock_tick'

        # test publish with payload that fails to validate
        if True:
            try:
                yield self.publish(topic, self._counter, 'Some unexpected arg type', options=PublishOptions(acknowledge=True))
            except Exception as e:
                if isinstance(e, ApplicationError) and e.error == 'wamp.error.invalid_argument':
                    if 'invalid type' not in e.args[0]:
                        raise RuntimeError('did not find expected error text in exception!')
                    else:
                        self.log.info('{func} - test case 1: ok, correct exception raised!', func=hltype(self._periodic))
                else:
                    self.log.failure()
                    raise RuntimeError('unexpected exception raised!')
            else:
                raise RuntimeError('invalid publish did not raise!')

        # test publish with valid payload. this validates against validation type:
        # trading.ClockTickSimple
        #
        if True:
            pub = yield self.publish(topic, self._counter, time_ns(), options=PublishOptions(acknowledge=True))
            self.log.info('{func} published to "{topic}" (publication_id={publication_id})', func=hltype(self._periodic),
                          topic=hlid(topic), publication_id=hlval(pub.id))

    # eth.pydefi.replica.<uuid:replica>.book.<uuid:book>.get_candle_history
    # com.example.private.replica.ba3b1e9f-3006-4eae-ae88-cf5896b36342.book.a17f0b45-1ed2-4b1a-9a7d-c112e8cd5d9b.get_candle_history
    @wamp.register('com.example.private.'
                   'replica.ba3b1e9f-3006-4eae-ae88-cf5896b36342.'
                   'book.a17f0b45-1ed2-4b1a-9a7d-c112e8cd5d9b.'
                   'get_candle_history',
                   check_types=True,
                   options=RegisterOptions(details=True))
    def get_candle_history(self, period_dur: int, start_ts: int, limit: Optional[int] = None, details: Optional[CallDetails] = None):
        self.log.info('{func} period_dur={period_dur}, start_ts={start_ts}, limit={limit}, details={details}', func=hltype(self.get_candle_history),
                      period_dur=hlval(period_dur), start_ts=hlval(start_ts), limit=hlval(limit), details=details)

        # data to return, valid according to validation type:
        # example4.bfs: trading.Candle
        candle = {
            'period_dur': 10,
            'start_ts': 1654900797173358641,
            'market_oid': os.urandom(16),
            'modified': 1654900797173358641,
            'quantity': 1.,
            'volume': 1.,
            'price_open': 1.,
            'price_close': 1.,
            'price_min': 1.,
            'price_max': 1.,
            'price_avg': 1.,
            'price_var': 1.,
            'price_avg_volw': 1.,
            'price_var_volw': 1.,
        }

        # for test purposes, depending on call arguments, make the returned result invalid
        # according to validation type:
        # example4.bfs: trading.CandleResult

        if period_dur == 6:
            # return invalid key in result
            candle['foobar_invalid'] = 'something'
        elif period_dur == 7:
            # return invalid value type for valid key in result
            candle['price_open'] = 'something'
        elif period_dur == 8:
            raise ApplicationError('com.example.error1', 'Something bad has happened!')
        else:  # period_dur >= 10
            # return a valid result
            pass

        # this will return WAMP result: args=[candle], kwargs=None
        return candle
