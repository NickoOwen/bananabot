import logging
from logging.config import fileConfig

#### Setup Logger ####
fileConfig('logging.conf', disable_existing_loggers=False)
logger = logging.getLogger(__name__)

def get_logger():
    return logger