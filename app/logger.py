import logging
from logging.config import fileConfig
from os import path

#### Setup Logger ####
log_file_path = path.join(path.dirname(path.abspath(__file__)), 'logging.conf')
fileConfig(log_file_path, disable_existing_loggers=False)
logger = logging.getLogger(__name__)

def get_logger():
    return logger