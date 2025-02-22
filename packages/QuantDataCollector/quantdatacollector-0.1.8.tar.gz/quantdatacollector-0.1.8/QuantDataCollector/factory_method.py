from QuantDataCollector.baostock_data_collector import BaostockDataCollector
from QuantDataCollector.data_collector_config import default_config
from QuantDataCollector.type import RequestFrequency, AdjustFlag, FilterType

class DataCollectorFactory:
    def __init__(self, main_object_type, config_dict = default_config):
        self.__main_object = eval(main_object_type)(config_dict)

    def get_stock_type(self, stock_code):
        return self.__main_object.get_stock_type(stock_code)

    def get_all_stock_code(self, day = None):
        return self.__main_object.get_all_stock_code(day)

    def get_all_share_code(self, day = None):
        return self.__main_object.get_all_share_code(day)

    def get_stock_basic_data(self, stock_code_list = [], filter = FilterType.NoFilter):
        return self.__main_object.get_stock_basic_data(stock_code_list, filter)

    def get_stock_data_period(self, stock_code_list, start=None, end=None, frequency=RequestFrequency.DayK, adjust_flag = AdjustFlag.NoAdjust):
        return self.__main_object.get_stock_data_period(stock_code_list, start, end, frequency, adjust_flag)

    def get_stock_data(self, stock_code_list, day=None, frequency=RequestFrequency.DayK, adjust_flag=AdjustFlag.NoAdjust):
        return self.__main_object.get_stock_data(stock_code_list, day,frequency, adjust_flag)

    def is_trade_day(self, day):
        return self.__main_object.is_trade_day(day)

    def get_recent_trade_day(self,day=None):
        return self.__main_object.get_recent_trade_day(day)

    def get_data_collector_info(self):
        return self.__main_object.get_data_collector_info()

    #def get_data_from_other_type(self, object_type, param):
        """从主数据类以外的类获取数据的写法
        """
        #return eval(object_type)().get_data_from_other_type(param)
