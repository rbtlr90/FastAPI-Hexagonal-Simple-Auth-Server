import logging
import logging.config
import os

LOGGER_TYPE = os.getenv('ENV', 'prod')
LOGGER_NAME = os.getenv('LOGGER_NAME', 'hidom-server')

logging.config.fileConfig("app/config/logging.conf")
logger = logging.getLogger(LOGGER_TYPE)
