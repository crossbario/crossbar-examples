
from twisted.internet.defer import inlineCallbacks

from autobahn import wamp
from autobahn.wamp.types import RegisterOptions
from autobahn.twisted.wamp import ApplicationSession


class ReportsBackend(ApplicationSession):

    def __init__(self, config):
        ApplicationSession.__init__(self, config)
        self.log.info('ReportsBackend.__init__(config={config})', config=config)
        self._counter = 0

    @inlineCallbacks
    def onJoin(self, details):
        self.log.info('ReportsBackend.onJoin(details={details})', details=details)
        regs = yield self.register(self, prefix='com.example.', options=RegisterOptions(details_arg='details'))
        self.log.info('ReportsBackend: registered {} procedures. ready!'.format(len(regs)))

    @wamp.register(None)
    def greeting(self, name, details=None):
        self._counter += 1
        self.log.info('ReportsBackend.greeting(name={name}, details={details})',
                        name=name, details=details)
        result = {
            'name': name,
            'message': 'Hello, "{}"! (counter={})'.format(name, self._counter)
        }
        return result

    @wamp.register(None)
    def get_product_report(self, product_id, report, year=None, month=None, details=None):
        self._counter += 1
        self.log.info('ReportsBackend.get_product_report(product_id={product_id}, report={report}, year={year}, month={month}, details={details})',
                        product_id=product_id, report=report, year=year, month=month, details=details)
        result = {
            'product_id': product_id,
            'report': report,
            'year': year,
            'month': month,
            'flasky': 'Hello, world! (counter={})'.format(self._counter)
        }
        return result
