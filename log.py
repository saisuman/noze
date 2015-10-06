import logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p')
_logger = logging.getLogger('noze')
d = _logger.debug
e = _logger.error
ex = _logger.exception
c = _logger.critical
w = _logger.warning
i = _logger.info

