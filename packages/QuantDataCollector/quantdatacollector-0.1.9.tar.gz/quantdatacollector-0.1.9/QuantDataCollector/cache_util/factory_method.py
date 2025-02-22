from QuantDataCollector.cache_util.pickle_cache_util import PickleCacheUtil
from QuantDataCollector.cache_util.mysql_cache_util import MysqlCacheUtil
from QuantDataCollector.cache_util.postgresql_cache_util import PostgresqlCacheUtil

class CacheUtilFactory:
    def __init__(self, main_object_type, config_dict):
        self.__main_object = eval(main_object_type)(config_dict)

    def has_stock_basic_cache(self, stock_code):
        return self.__main_object.has_stock_basic_cache(stock_code)

    def get_stock_basic_data(self, stock_code):
        return self.__main_object.get_stock_basic_data(stock_code)

    def has_stock_cache(self, stock_code, date, frequency = 'd', adjust_flag = 2):
        return self.__main_object.has_stock_cache(stock_code, date, frequency, adjust_flag)

    def get_stock_data(self, stock_code, date, frequency = 'd', adjust_flag = 2):
        return self.__main_object.get_stock_data(stock_code, date, frequency, adjust_flag)

    def has_batch_cache(self, stock_code, start, end, frequency = 'd', adjust_flag = 2):
        return self.__main_object.has_batch_cache(stock_code, start, end, frequency, adjust_flag)

    def get_stock_data_batch(self, stock_code, start, end, frequency = 'd', adjust_flag = 2):
        return self.__main_object.get_stock_data_batch(stock_code, start, end, frequency, adjust_flag)

    def save_stock_data(self, stock_code, date, data, frequency):
        return self.__main_object.save_stock_data(stock_code, date, data, frequency)

    def save_stock_basic_data(self, stock_code, data):
        return self.__main_object.save_stock_basic_data(stock_code, data)

    def delete_stock_basic_data(self, stock_code):
        return self.__main_object.delete_stock_basic_data(stock_code)

    def delete_stock_data(self, stock_code, date, frequency, adjust_flag):
        return self.__main_object.delete_stock_data(stock_code, date, frequency, adjust_flag)

    def clear_basic_cache(self):
        return self.__main_object.clear_basic_cache()

    def clear_full_cache(self):
        return self.__main_object.clear_full_cache()

    def cache_info(self):
        return self.__main_object.cache_info()
