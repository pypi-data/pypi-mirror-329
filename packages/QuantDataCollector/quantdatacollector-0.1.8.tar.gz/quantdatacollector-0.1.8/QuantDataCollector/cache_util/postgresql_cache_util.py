import os
import pickle
import logging
import atexit
import signal
import datetime

from QuantDataCollector.cache_util.abstract_cache_util import AbstractCacheUtil
from QuantDataCollector.cache_util.abstract_cache_util import CacheUtilError
from QuantDataCollector.cache_util.cache_util_config import default_config
from QuantDataCollector.Utils.file_utils import mkdir
from QuantDataCollector.Utils.baostock_utils import is_trade_day
from QuantDataCollector.Utils.utils import date_compare,\
                                date_add_zero_padding,\
                                date_increase,\
                                date_format
from QuantDataCollector.Utils.database_utils.postgresql_utils import postgresqlOps
from QuantDataCollector.Global.settings import RESULTS_ROOT_PATH,\
                                    LOGGING_FILE_DIR,\
                                    LOGGING_FILE_NAME
                                    
from QuantDataCollector.Global.settings import MYSQL_STOCK_BAISC_DATA_TABLE_NAME,\
                                    MYSQL_STOCK_DAY_K_DATA_TABLE_NAME

class PostgresqlCacheUtil(AbstractCacheUtil):
    __config = {}

    def __init__(self, config_dict = default_config):
        self.__config = config_dict
        signal.signal(signal.SIGINT, self.signal_exit)
        if "log" in config_dict:
            self.__config_logging(int(config_dict["log"])) # 配置logging
        else:
            self.__config_logging() # 配置logging

        self.db = postgresqlOps(database="postgres")

    def signal_exit(self,signum,frame):
        self.__logger.info("my_exit: interrupted by ctrl+c")
        exit()

    def __config_logging(self, level =logging.WARNING):
        if level == logging.DEBUG:
            print("================ cache_util info =====================")
            print(self.cache_info())
            print("============= end of cache_util info =================")

        self.__logger = logging.getLogger('postgresql_cache_util')
        
        if not os.path.exists(LOGGING_FILE_DIR):
            mkdir(LOGGING_FILE_DIR)
        ch = logging.FileHandler(LOGGING_FILE_NAME)
        formatter = logging.Formatter(fmt='%(asctime)s.%(msecs)03d - %(name)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
        ch.setFormatter(formatter)
        self.__logger.addHandler(ch)
        self.__logger.setLevel(level)

    def has_stock_basic_cache(self, stock_code):
        filter_condition = "code = '" + stock_code + "'"
        res, count = self.db.data_num(MYSQL_STOCK_BAISC_DATA_TABLE_NAME,filter_condition)
        return count > 0

    def get_stock_basic_data(self, stock_code):
        filter_condition = "code = '" + stock_code + "'"
        succ, res =  self.db.query(MYSQL_STOCK_BAISC_DATA_TABLE_NAME, filter_condition = filter_condition)
        retval = {}
        if succ:
            column_names = self.db.get_table_columns(MYSQL_STOCK_BAISC_DATA_TABLE_NAME)
            if len(res[0]) > 0 and len(column_names) == len(res[0]):
                for idx, col in enumerate(column_names):
                    if isinstance(res[0][idx], datetime.date):
                        retval[col] = res[0][idx].strftime('%Y-%m-%d')
                    else:
                        retval[col] = res[0][idx]
        return retval


    def has_stock_cache(self, stock_code, date):
        """判断单条数据是否有缓存
        Returns:
          bool:
        """
        filter_condition = "code = '" + stock_code + "' AND date = '" + date + "'"
        res, count = self.db.data_num(MYSQL_STOCK_DAY_K_DATA_TABLE_NAME,filter_condition)
        return count > 0

    def get_stock_data(self, stock_code, date):
        """获取单条数据

        Args:
          date: String，日期。需要注意的是2022-1-2等价于2022-01-02

        Returns:
          Dictionary: 数据index及其内容
        """
        filter_condition = "code = '" + stock_code + "' AND date = '" + date + "'"
        succ, res =  self.db.query(MYSQL_STOCK_DAY_K_DATA_TABLE_NAME, filter_condition = filter_condition)
        retval = {}
        if succ:
            column_names = self.db.get_table_columns(MYSQL_STOCK_DAY_K_DATA_TABLE_NAME)
            if len(res) > 0 and len(res[0]) > 0 and len(column_names) == len(res[0]):
                for idx, col in enumerate(column_names):
                    if isinstance(res[0][idx], datetime.date):
                        retval[col] = res[0][idx].strftime('%Y-%m-%d')
                    else:
                        retval[col] = res[0][idx]
        return retval

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
            if is_trade_day(day) and not self.has_stock_cache(stock_code, day):
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
        """保存某股票某天的数据

        将指定股票某天的数据保存到缓存

        Args:
          stock_code: String，股票代码
          data: dict，数据index及其数值

        Returns:
          bool: 保存成功返回True
        """
        if "date" not in data and date_format(date):
            data["date"] = date

        if "code" not in data:
            data["code"] = stock_code

        res, msg = self.db.insert(MYSQL_STOCK_DAY_K_DATA_TABLE_NAME,data)
        if(res):
            return True
        else:
            return False

    def save_stock_basic_data(self, stock_code, data):
        if "code" not in data:
            data["code"] = stock_code

        res, msg = self.db.insert(MYSQL_STOCK_BAISC_DATA_TABLE_NAME,data)
        if res:
            return True
        else:
            return False

    def delete_stock_basic_data(self, stock_code):
        filter_condition = "code = '" + stock_code + "'"
        res, msg = self.db.delete(MYSQL_STOCK_BAISC_DATA_TABLE_NAME,filter_condition)
        if res:
            return True
        else:
            return False

    def delete_stock_data(self, stock_code, date):
        filter_condition = "code = '" + stock_code + "'"
        if date:
            filter_condition += " AND date = '" + date + "'"
        res, msg = self.db.delete(MYSQL_STOCK_DAY_K_DATA_TABLE_NAME,filter_condition)
        if res:
            return True
        else:
            return False

    def clear_basic_cache(self):
        pass

    def clear_full_cache(self):
        return True

    def cache_info(self):
        res = ""
        res += "cache type: PostgreSQL Database\n"
        res += "config: " + str(self.__config)
        return res

if __name__ == '__main__':
    cache_util = PostgresqlCacheUtil()
    #print(cache_util.has_stock_basic_cache("sh.600000"))
    #print(cache_util.get_stock_basic_data("sh.600000"))
    #print(cache_util.has_stock_cache("sh.600000","2022-06-29"))
    #print(cache_util.get_stock_data("sh.600000","2022-06-29"))
    #print(cache_util.has_batch_cache("sh.600000","2022-06-20", "2022-07-04"))
    #print(cache_util.get_stock_data_batch("sh.600000","2022-06-20", "2022-07-04"))
    #cache_util.delete_stock_data("sh.600000","2022-06-20")
