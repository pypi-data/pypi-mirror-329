import os
import pickle
import logging
import atexit
import signal

from QuantDataCollector.cache_util.abstract_cache_util import AbstractCacheUtil
from QuantDataCollector.cache_util.abstract_cache_util import CacheUtilError
from QuantDataCollector.cache_util.cache_util_config import default_config

from QuantDataCollector.Utils.file_utils import mkdir
from QuantDataCollector.Utils.baostock_utils import is_trade_day
from QuantDataCollector.Utils.utils import date_compare, date_add_zero_padding, date_increase
from QuantDataCollector.Global.settings import RESULTS_ROOT_PATH,\
                                    LOGGING_FILE_DIR,\
                                    LOGGING_FILE_NAME

class PickleCacheUtil(AbstractCacheUtil):
    """存储的数据结构为：
    basic:
      {(stock_code, date):{'name':'上证50', 'type':'2', 'status':'0'},(stock_code, date):{},...}
    full:
      {(stock_code, date):{'open':10.0, 'close':11.1},(stock_code, date):{},...}
    """
    __basic_cache_data = {}
    __full_cache_data = {}
    __config = {}

    def __init__(self, config_dict = default_config):
        self.__config = config_dict
        signal.signal(signal.SIGINT, self.signal_exit)
        if "log" in config_dict:
            self.__config_logging(int(config_dict["log"])) # 配置logging
        else:
            self.__config_logging() # 配置logging
        data_dir = RESULTS_ROOT_PATH + "/pickle_cache_data/"
        self.__basic_data_file_name = data_dir + "basic_cache_data.pkl"
        self.__full_data_file_name = data_dir + "full_cache_data.pkl"
        if not os.path.exists(data_dir):
            mkdir(data_dir)

        if os.path.exists(self.__basic_data_file_name) and os.path.getsize(self.__basic_data_file_name) > 0:
            with open(self.__basic_data_file_name, 'rb') as fb:
                try:
                    self.__basic_cache_data = pickle.load(fb)
                except BaseException as e:
                    self.__logger.exception(e)
                    self.__logger.critical("__init__: pickle load basic data fail, file name:" + self.__basic_data_file_name)
                    raise CacheUtilError("load basic data error")
                    exit()

        if os.path.exists(self.__full_data_file_name) and os.path.getsize(self.__full_data_file_name) > 0:
            with open(self.__full_data_file_name, 'rb') as ff:
                try:
                    self.__full_cache_data = pickle.load(ff)
                except BaseException as e:
                    self.__logger.exception(e)
                    self.__logger.critical("__init__: pickle load full data fail, file name:" + self.__full_data_file_name)
                    raise CacheUtilError("load full data error")
                    exit()

        atexit.register(self.save_data_before_leave)
        """注册exit时要执行的函数不在__del__中做，是因为__del__中使用open会报错"""

    def signal_exit(self,signum,frame):
        self.__logger.info("my_exit: interrupted by ctrl+c")
        self.save_data_before_leave()
        exit()

    def save_data_before_leave(self):
        with open(self.__basic_data_file_name, 'wb') as basic_f:
            self.__logger.info("save_data_before_leave: basic_data keys number is {}".format(len(self.__basic_cache_data.keys())))
            pickle.dump(self.__basic_cache_data, basic_f,protocol=pickle.HIGHEST_PROTOCOL)

        with open(self.__full_data_file_name, 'wb') as full_f:
            self.__logger.info("save_data_before_leave: full_data keys number is {}".format(len(self.__full_cache_data.keys())))
            pickle.dump(self.__full_cache_data, full_f,protocol=pickle.HIGHEST_PROTOCOL)

    def __config_logging(self, level =logging.WARNING):
        if level == logging.DEBUG:
            print("================ cache_util info =====================")
            print(self.cache_info())
            print("============= end of cache_util info =================")

        self.__logger = logging.getLogger('pickle_cache_util')
        
        if not os.path.exists(LOGGING_FILE_DIR):
            mkdir(LOGGING_FILE_DIR)
        ch = logging.FileHandler(LOGGING_FILE_NAME)
        formatter = logging.Formatter(fmt='%(asctime)s.%(msecs)03d - %(name)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
        ch.setFormatter(formatter)
        self.__logger.addHandler(ch)
        self.__logger.setLevel(level)

    def has_stock_basic_cache(self, stock_code):
        return stock_code in self.__basic_cache_data.keys()

    def get_stock_basic_data(self, stock_code):
        if not self.has_stock_basic_cache(stock_code):
            self.__logger.warning("get_stock_basic_data: 试图获取没有的数据 stock_code = " + stock_code)
            return {}
        return self.__basic_cache_data[stock_code]


    def has_stock_cache(self, stock_code, date):
        """判断单条数据是否有缓存
        Returns:
          bool:
        """
        date = date_add_zero_padding(date)
        return (stock_code, date) in self.__full_cache_data.keys()

    def get_stock_data(self, stock_code, date):
        """获取单条数据

        Args:
          date: String，日期。需要注意的是2022-1-2等价于2022-01-02

        Returns:
          Dictionary: 数据index及其内容
        """
        date = date_add_zero_padding(date)
        if not self.has_stock_cache(stock_code, date):
            self.__logger.warning("get_stock_data: 试图获取没有的数据 stock_code = " + stock_code + "date = " + date)
            return {}
        return self.__full_cache_data[(stock_code, date)]

    def has_batch_cache(self, stock_code, start, end):
        """判断批量数据是否有缓存

        Returns:
          bool:
        """
        start = date_add_zero_padding(start)
        end = date_add_zero_padding(end)
        if date_compare(start, end) == 1:
            self.__logger.warning("has_batch_cache:开始日期大于结束日期")
            return False

        day = start
        while date_compare(day, end) <= 0: # day <= end
            if is_trade_day(day) and  not self.has_stock_cache(stock_code, day):
                self.__logger.info("has_batch_cache: stock_code: " + stock_code + " " + day + "没有缓存数据")
                return False
            day = date_increase(day)
        return True

    def get_stock_data_batch(self, stock_code, start, end):
        """批量获取数据
        """
        start = date_add_zero_padding(start)
        end = date_add_zero_padding(end)
        if date_compare(start, end) == 1:
            self.__logger.warning("get_stock_cache_batch:开始日期大于结束日期")
            return []

        res_list = {}
        day = start
        while date_compare(day, end) <= 0: # day <= end
            if is_trade_day(day):
                res_list[day] = self.get_stock_data(stock_code, day)
            day = date_increase(day)
        return res_list

    def save_stock_data(self, stock_code, date, data):
        date = date_add_zero_padding(date)
        self.__full_cache_data[(stock_code, date)] = data
        self.__save_full_data_to_file_if_need()
        return True

    def save_stock_basic_data(self, stock_code, data):
        self.__basic_cache_data[stock_code] = data
        self.__save_basic_data_to_file_if_need()
        return True

    def __save_basic_data_to_file(self):
        with open(self.__basic_data_file_name, 'wb') as basic_f:
            self.__logger.info("__save_basic_data_to_file: basic_data keys number is {}".format(len(self.__basic_cache_data.keys())))
            pickle.dump(self.__basic_cache_data, basic_f)

    def __save_basic_data_to_file_if_need(self):
        """每存储一定数量的数据，就写入file"""
        if len(self.__basic_cache_data.keys()) % 100 != 0:
            return
        self.__save_basic_data_to_file()

    def __save_full_data_to_file(self):
        with open(self.__full_data_file_name, 'wb') as full_f:
            self.__logger.info("__save_full_data_to_file: full_data keys number is {}".format(len(self.__full_cache_data.keys())))
            pickle.dump(self.__full_cache_data, full_f)

    def __save_full_data_to_file_if_need(self):
        """每存储一定数量的数据，就写入file"""
        if len(self.__full_cache_data.keys()) % 100 != 0:
            return
        self.__save_full_data_to_file()

    def delete_stock_basic_data(self, stock_code):
        if stock_code not in self.__basic_cache_data:
            return False
        self.__logger.info("delete_stock_basic_data, stock code is %s", stock_code)
        try:
            self.__basic_cache_data.pop(stock_code)
            self.__save_basic_data_to_file()
        except:
            return False
        return True

    def delete_stock_data(self, stock_code, date):
        if (stock_code, date) not in self.__full_cache_data:
            return False
        self.__logger.info("delete_full_basic_data, stock code is %s, date is %s", stock_code, date)
        try:
            self.__full_cache_data.pop((stock_code, date))
            self.__save_full_data_to_file()
        except:
            return False
        return True

    def clear_basic_cache(self):
        self.__logger.info("clear_basic_data")
        try:
            self.__basic_cache_data.clear()
            self.__save_basic_data_to_file()
        except:
            return False
        return True

    def clear_full_cache(self):
        self.__logger.info("clear_full_data")
        try:
            self.__full_cache_data.clear()
            self.__save_full_data_to_file()
        except:
            return False
        return True

    def cache_info(self):
        res = ""
        res += "cache type: pickle\n"
        res += "cache path:"
        res += RESULTS_ROOT_PATH + "/pickle_cache_data/\n"
        res += "config: " + str(self.__config)
        return res

if __name__ == '__main__':
    cache_util = PickleCacheUtil()
    #cache_util.save_stock_basic_data("sh.600000","2021-1-1")
    print(cache_util.has_stock_basic_cache("sh.600000"))
    print(LOGGING_FILE_DIR)
