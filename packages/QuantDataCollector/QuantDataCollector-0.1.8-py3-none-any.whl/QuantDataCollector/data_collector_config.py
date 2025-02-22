from enum import Enum, IntEnum
import logging

class cache_config (Enum):
    NO_CACHE = 1
    PICKLE_CACHE = 2
    MYSQL_CACHE = 3
    POSTGRESQL_CACHE = 3
    
class log_config (IntEnum):
    CRITICAL_LOG = logging.CRITICAL
    ERROR_LOG = logging.ERROR
    WARNING_LOG = logging.WARNING
    INFO_LOG = logging.INFO
    DEBUG_LOG = logging.DEBUG
    NO_LOG = logging.NOTSET

default_config = {
        "cache" : cache_config.NO_CACHE,
        "log" : log_config.WARNING_LOG}

