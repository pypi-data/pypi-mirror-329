from QuantDataCollector.cache_util.factory_method import CacheUtilFactory
from QuantDataCollector.data_collector_config import default_config,\
        cache_config

class CacheUtil:
    def __init__(self, config_dict = default_config):
        assert "cache" in config_dict, "配置中没有cache项，无法初始化CacheUtil"
        if config_dict["cache"] == cache_config.PICKLE_CACHE:
            self.__df = CacheUtilFactory("PickleCacheUtil", config_dict)
        elif config_dict["cache"] == cache_config.MYSQL_CACHE:
            self.__df = CacheUtilFactory("MysqlCacheUtil", config_dict)
        elif config_dict["cache"] == cache_config.POSTGRESQL_CACHE:
            self.__df = CacheUtilFactory("PostgresqlCacheUtil", config_dict)
        else:
            assert False, "暂时不支持cache 配置：" + config_dict["cache"]

    def has_stock_basic_cache(self, stock_code):
        return self.__df.has_stock_basic_cache(stock_code)

    def get_stock_basic_data(self, stock_code):
        return self.__df.get_stock_basic_data(stock_code)

    def has_stock_cache(self, stock_code, date, frequency = 'd', adjust_flag = 2):
        return self.__df.has_stock_cache(stock_code, date, frequency, adjust_flag)

    def get_stock_data(self, stock_code, date, frequency = 'd', adjust_flag = 2):
        return self.__df.get_stock_data(stock_code, date, frequency, adjust_flag)

    def has_batch_cache(self, stock_code, start, end, frequency = 'd', adjust_flag = 2):
        return self.__df.has_batch_cache(stock_code, start, end, frequency, adjust_flag)

    def get_stock_data_batch(self, stock_code, start, end, frequency = 'd', adjust_flag = 2):
        return self.__df.get_stock_data_batch(stock_code, start, end, frequency, adjust_flag)

    def save_stock_data(self, stock_code, date, data, frequency):
        return self.__df.save_stock_data(stock_code, date, data, frequency)

    def save_stock_basic_data(self, stock_code, data):
        return self.__df.save_stock_basic_data(stock_code, data)

    def delete_stock_basic_data(self, stock_code):
        return self.__df.delete_stock_basic_data(stock_code)

    def delete_stock_data(self, stock_code, date, frequency, adjust_flag):
        return self.__df.delete_stock_data(stock_code, date, frequency, adjust_flag)

    def clear_basic_cache(self):
        return self.__df.clear_basic_cache()

    def clear_full_cache(self):
        return self.__df.clear_full_cache()

    def cache_info(self):
        return self.__df.cache_info()

if __name__ == '__main__':
    cache_util = CacheUtil()
    #cache_util.save_stock_basic_data("sh.600000","2021-1-1")
    print(cache_util.has_stock_basic_cache("sh.600000"))
