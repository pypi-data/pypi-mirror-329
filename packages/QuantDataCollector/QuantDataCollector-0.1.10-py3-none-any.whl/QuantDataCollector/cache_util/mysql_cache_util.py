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
from QuantDataCollector.Utils.database_utils.mysql_utils import mysqlOps
from QuantDataCollector.Global.settings import RESULTS_ROOT_PATH,\
                                    LOGGING_FILE_DIR,\
                                    LOGGING_FILE_NAME
                                    
from QuantDataCollector.Global.settings import  \
                                    MYSQL_STOCK_DATABASE_NAME,\
                                    MYSQL_STOCK_BAISC_DATA_TABLE_NAME,\
                                    MYSQL_STOCK_MINUTE_K_DATA_TABLE_NAME, \
                                    MYSQL_STOCK_DAY_K_DATA_TABLE_NAME, \
                                    MYSQL_STOCK_WEEK_K_DATA_TABLE_NAME, \
                                    MYSQL_STOCK_MONTH_K_DATA_TABLE_NAME
frequency2tablename = {
    '5': MYSQL_STOCK_MINUTE_K_DATA_TABLE_NAME,
    '15': MYSQL_STOCK_MINUTE_K_DATA_TABLE_NAME,
    '30': MYSQL_STOCK_MINUTE_K_DATA_TABLE_NAME,
    '60': MYSQL_STOCK_MINUTE_K_DATA_TABLE_NAME,
    'd': MYSQL_STOCK_DAY_K_DATA_TABLE_NAME,
    'w': MYSQL_STOCK_WEEK_K_DATA_TABLE_NAME,
    'm': MYSQL_STOCK_MONTH_K_DATA_TABLE_NAME,
}

class MysqlCacheUtil(AbstractCacheUtil):
    __config = {}

    def __init__(self, config_dict = default_config):
        self.__config = config_dict
        signal.signal(signal.SIGINT, self.signal_exit)
        if "log" in config_dict:
            self.__config_logging(int(config_dict["log"])) # 配置logging
        else:
            self.__config_logging() # 配置logging

        self.db = mysqlOps(port=3307)
        if not self.db.is_database_exist(MYSQL_STOCK_DATABASE_NAME):
            self.db.create_database(MYSQL_STOCK_DATABASE_NAME)
        self.db.select_database(MYSQL_STOCK_DATABASE_NAME)
        self.__create_tables()

    def signal_exit(self,signum,frame):
        self.__logger.info("my_exit: interrupted by ctrl+c")
        exit()

    def __config_logging(self, level =logging.WARNING):
        if level == logging.DEBUG:
            print("================ cache_util info =====================")
            print(self.cache_info())
            print("============= end of cache_util info =================")

        self.__logger = logging.getLogger('mysql_cache_util')
        
        if not os.path.exists(LOGGING_FILE_DIR):
            mkdir(LOGGING_FILE_DIR)
        ch = logging.FileHandler(LOGGING_FILE_NAME)
        formatter = logging.Formatter(fmt='%(asctime)s.%(msecs)03d - %(name)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
        ch.setFormatter(formatter)
        self.__logger.addHandler(ch)
        self.__logger.setLevel(level)

    def __create_tables(self):
        self.db.create_table(MYSQL_STOCK_BAISC_DATA_TABLE_NAME,
            [{"name":"code", "type":"CHAR(10)", "postfix":["PRIMARY KEY", "NOT NULL"]},
             {"name":"code_name", "type":"VARCHAR(15)", "postfix":["NOT NULL"]},
             {"name":"ipoDate", "type":"DATE"},
             {"name":"outDate", "type":"DATE"},
             {"name":"type", "type":"TINYINT"},
             {"name":"status", "type":"TINYINT"}]
            )

        self.db.create_table(MYSQL_STOCK_MINUTE_K_DATA_TABLE_NAME,
            [{"name":"id", "type":"BIGINT", "postfix":["PRIMARY KEY", "NOT NULL", "AUTO_INCREMENT"]},
             {"name":"date", "type":"DATE", "postfix":["NOT NULL"]},
             {"name":"code", "type":"CHAR(10)", "postfix":["NOT NULL"]},
             {"name":"adjust_flag", "type":"TINYINT"},
             {"name":"time", "type":"TIME", "postfix":["NOT NULL"]},
             {"name":"open", "type":"FLOAT"},
             {"name":"high", "type":"FLOAT"},
             {"name":"low", "type":"FLOAT"},
             {"name":"close", "type":"FLOAT"},
             {"name":"volume", "type":"BIGINT"},
             {"name":"amount", "type":"FLOAT"}],
            ["code", MYSQL_STOCK_BAISC_DATA_TABLE_NAME, "code"],["code", "adjust_flag", "date","time"])

        self.db.create_table(MYSQL_STOCK_DAY_K_DATA_TABLE_NAME,
            [{"name":"id", "type":"BIGINT", "postfix":["PRIMARY KEY", "NOT NULL", "AUTO_INCREMENT"]},
             {"name":"code", "type":"CHAR(10)", "postfix":["NOT NULL"]},
             {"name":"date", "type":"DATE", "postfix":["NOT NULL"]},
             {"name":"adjust_flag", "type":"TINYINT"},
             {"name":"open", "type":"FLOAT"},
             {"name":"high", "type":"FLOAT"},
             {"name":"low", "type":"FLOAT"},
             {"name":"close", "type":"FLOAT"},
             {"name":"preclose", "type":"FLOAT"},
             {"name":"volume", "type":"BIGINT"},
             {"name":"amount", "type":"FLOAT"},
             {"name":"turn", "type":"FLOAT"},
             {"name":"trade_status", "type":"TINYINT"},
             {"name":"change_percent", "type":"FLOAT"},
             {"name":"pe_TTM", "type":"FLOAT"},
             {"name":"ps_TTM", "type":"FLOAT"},
             {"name":"pcf_ncf_TTM", "type":"FLOAT"},
             {"name":"pb_MRQ", "type":"FLOAT"},
             {"name":"is_ST", "type":"TINYINT"}],
            ["code", MYSQL_STOCK_BAISC_DATA_TABLE_NAME, "code"], ["code", "date", "adjust_flag"])

        self.db.create_table(MYSQL_STOCK_WEEK_K_DATA_TABLE_NAME,
            [{"name":"id", "type":"BIGINT", "postfix":["PRIMARY KEY", "NOT NULL", "AUTO_INCREMENT"]},
             {"name":"code", "type":"CHAR(10)", "postfix":["NOT NULL"]},
             {"name":"date", "type":"DATE", "postfix":["NOT NULL"]},
             {"name":"adjust_flag", "type":"TINYINT"},
             {"name":"open", "type":"FLOAT"},
             {"name":"high", "type":"FLOAT"},
             {"name":"low", "type":"FLOAT"},
             {"name":"close", "type":"FLOAT"},
             {"name":"volume", "type":"BIGINT"},
             {"name":"amount", "type":"FLOAT"},
             {"name":"turn", "type":"FLOAT"},
             {"name":"change_percent", "type":"FLOAT"}],
            ["code", MYSQL_STOCK_BAISC_DATA_TABLE_NAME, "code"], ["code", "date", "adjust_flag"])

        self.db.create_table(MYSQL_STOCK_MONTH_K_DATA_TABLE_NAME,
            [{"name":"id", "type":"BIGINT", "postfix":["PRIMARY KEY", "NOT NULL", "AUTO_INCREMENT"]},
             {"name":"code", "type":"CHAR(10)", "postfix":["NOT NULL"]},
             {"name":"date", "type":"DATE", "postfix":["NOT NULL"]},
             {"name":"adjust_flag", "type":"TINYINT"},
             {"name":"open", "type":"FLOAT"},
             {"name":"high", "type":"FLOAT"},
             {"name":"low", "type":"FLOAT"},
             {"name":"close", "type":"FLOAT"},
             {"name":"volume", "type":"BIGINT"},
             {"name":"amount", "type":"FLOAT"},
             {"name":"turn", "type":"FLOAT"},
             {"name":"change_percent", "type":"FLOAT"}],
            ["code", MYSQL_STOCK_BAISC_DATA_TABLE_NAME, "code"], ["code", "date", "adjust_flag"])

    def has_stock_basic_cache(self, stock_code):
        self.__logger.info("has_stock_basic_cache: stock_code = " + str(stock_code))
        filter_condition = "code = '" + stock_code + "'"
        res, count = self.db.data_num(MYSQL_STOCK_BAISC_DATA_TABLE_NAME,filter_condition)
        return count > 0

    def get_stock_basic_data(self, stock_code):
        if not self.has_stock_basic_cache(stock_code):
            return  {}

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

    def has_stock_cache(self, stock_code, date, frequency, adjust_flag):
        """判断单条数据是否有缓存
        Returns:
          bool:
        """
        current_table_name = frequency2tablename[frequency]
        target_num = 1

        filter_condition = "code = '" + stock_code + "' AND date = '" + date + "'"
        if adjust_flag:
            filter_condition = filter_condition + " AND adjust_flag = " + str(adjust_flag) + ""
        if frequency == '5' or frequency == '15' or frequency == '30' or frequency == '60':
            # 交易时间9:30 - 11:30， 13:00 - 15:00共4个小时
            filter_condition = filter_condition + " AND MINUTE(time) % " + frequency + "= 0"
            target_num = 240 / int(frequency)
        res, count = self.db.data_num(current_table_name,filter_condition)
        return count >= target_num

    def get_stock_data(self, stock_code, date, frequency, adjust_flag):
        """获取单条数据

        Args:
          date: String，日期。需要注意的是2022-1-2等价于2022-01-02

        Returns:
          List: 每个元素为数据index及其内容 
        """
        current_table_name = frequency2tablename[frequency]

        filter_condition = "code = '" + stock_code + "' AND date = '" + date + "'"
        if adjust_flag:
            filter_condition = filter_condition + " AND adjust_flag = '" + str(adjust_flag) + "'"
        if frequency == '5' or frequency == '15' or frequency == '30' or frequency == '60':
            # 交易时间9:30 - 11:30， 13:00 - 15:00共4个小时
            filter_condition = filter_condition + " AND MINUTE(time) % " + frequency + "= 0"

        succ, res =  self.db.query(current_table_name, filter_condition = filter_condition)
        result = []
        if succ:
            column_names = self.db.get_table_columns(current_table_name)
            for r in res:
                retval = {}
                if len(column_names) == len(r):
                    for idx, col in enumerate(column_names):
                        if col == 'date':
                            retval[col] = r[idx].strftime('%Y-%m-%d')
                        elif col == 'time':
                            # 计算总小时数（包含天数转换的小时）
                            total_hours = r[idx].days * 24 + r[idx].seconds // 3600
                            # 剩余秒数（扣除已计算的小时部分）
                            remaining_seconds = r[idx].seconds % 3600
                            # 分解分钟、秒和毫秒
                            minutes = remaining_seconds // 60
                            seconds = remaining_seconds % 60
                            milliseconds = r[idx].microseconds // 1000  # 微秒转毫秒
                            # 格式化为 HH:MM:SS.fff
                            retval[col] = f"{total_hours:02}:{minutes:02}:{seconds:02}.{milliseconds:03d}"
                        elif col == 'id':
                            continue
                        else:
                            retval[col] = r[idx]
                result.append(retval)
        return result

    def has_batch_cache(self, stock_code, start, end, frequency, adjust_flag):
        """判断批量数据是否有缓存

        Returns:
          bool:
        """
        return False # 暂时停用周期数据获取的缓存支持

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

    def get_stock_data_batch(self, stock_code, start, end, frequency, adjust_flag):
        """批量获取数据
        """
        return # 暂时停用周期数据获取的缓存支持

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

    def save_stock_data(self, stock_code, date, data, frequency):
        """保存某股票某天的数据

        将指定股票某天的数据保存到缓存

        Args:
          stock_code: String，股票代码
          data: dict，数据index及其数值

        Returns:
          bool: 保存成功返回True
        """
        current_table_name = frequency2tablename[frequency]

        if "code" not in data:
            data["code"] = stock_code

        res, msg = self.db.insert(current_table_name, data)
        if(res):
            return True
        else:
            return False

    def save_stock_basic_data(self, stock_code, data):
        if "code" not in data:
            data["code"] = stock_code

        res, msg = self.db.insert(MYSQL_STOCK_BAISC_DATA_TABLE_NAME,data)
        if(res):
            return True
        else:
            return False

    def delete_stock_basic_data(self, stock_code):
        pass

    def delete_stock_data(self, stock_code, date, frequency, adjust_flag):
        pass

    def clear_basic_cache(self):
        pass

    def clear_full_cache(self):
        return True

    def cache_info(self):
        res = ""
        res += "cache type: MySQL Database\n"
        res += "config: " + str(self.__config)
        return res

if __name__ == '__main__':
    cache_util = MysqlCacheUtil()
    print(cache_util.has_stock_basic_cache("sh.600000"))
    print(cache_util.get_stock_basic_data("sh.600000"))
    # 获取当前时间以秒为单位
    
    # 将秒转换为格式化日期字符串
    # formatted_date = datetime.datetime.utcfromtimestamp(current_time).strftime("%Y-%m-%d %H:%M:%S")

    # cache_util.save_stock_basic_data("sh.600000", {"code":"sh.600000",
                                                #    "name":"测试名",
                                                #    "ipo_date":"1992-01-23",
                                                #    "out_date":"2000-2-03",
                                                #    "type": 1,
                                                #    "status": 2
                                                #    })
    # print(cache_util.has_stock_basic_cache("sh.600000"))
    # print(cache_util.get_stock_basic_data("sh.600000"))


    print(cache_util.has_stock_cache("sh.600000","2022-01-20",'5', 2))
    print(cache_util.get_stock_data("sh.600000","2022-01-20", '5', 2))

    """
    print(cache_util.save_stock_data("sh.600000", "2022-06-29",{
                                                   "code":"sh.600000",
                                                   "date":"2022-06-29",
                                                   "adjust_flag": 2,
                                                #    "time": formatted_date,
                                                   "open":1.23,
                                                   "high":4.56,
                                                   "low":2.23,
                                                   "close":6.23,
                                                   "preclose":7.23,
                                                   "volume":1234567,
                                                   "amount":1234.678,
                                                   "turn":0.1,
                                                   "trade_status": 1,
                                                   "change_percent":1.2,
                                                   "pe_TTM":0.33,
                                                   "ps_TTM":0.44,
                                                   "pcf_ncf_TTM":0.55,
                                                   "pb_MRQ":0.66,
                                                   "is_ST":1
                                                   },'d'))
    print(cache_util.has_stock_cache("sh.600000","2022-06-29",'d', 1))
    print(cache_util.get_stock_data("sh.600000","2022-06-29", 'd', 1))
    # print(cache_util.has_batch_cache("sh.600000","2022-06-20", "2022-07-04"))
    # print(cache_util.get_stock_data_batch("sh.600000","2022-06-20", "2022-07-04"))
    """
