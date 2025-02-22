from enum import IntEnum
import logging

class log_config (IntEnum):
    CRITICAL_LOG = logging.CRITICAL
    ERROR_LOG = logging.ERROR
    WARNING_LOG = logging.WARNING
    INFO_LOG = logging.INFO
    DEBUG_LOG = logging.DEBUG
    NO_LOG = logging.NOTSET

default_config = {"log" : log_config.WARNING_LOG}

