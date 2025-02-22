from .data_collector import DataCollector
from .cache_util.cache_util import CacheUtil
from .data_collector_config import log_config, cache_config
from .type import RequestFrequency, AdjustFlag, FilterType
import sys

#__all__ = ['DataCollector', 'CacheUtil']

module = sys.modules[__name__] = DataCollector
module.log_config = log_config
module.cache_config = cache_config
module.RequestFrequency = RequestFrequency
module.AdjustFlag = AdjustFlag
module.FilterType = FilterType
