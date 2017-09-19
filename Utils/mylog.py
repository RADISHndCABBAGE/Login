import logging.config

logging.config.fileConfig('../Conf/logger.conf')
log = logging.getLogger('mylog')