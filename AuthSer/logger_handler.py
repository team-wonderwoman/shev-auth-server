import logging

logging.basicConfig(level=logging.DEBUG)

logger = logging.getLogger('authlogger')

class LoggerHandler:
    def __init__(self):
        self.logger = logging.getLogger('authlogger')
        self.logger.info('LoggerHandler.__init__is called')

#    def error_log(self, state_code, msg):

