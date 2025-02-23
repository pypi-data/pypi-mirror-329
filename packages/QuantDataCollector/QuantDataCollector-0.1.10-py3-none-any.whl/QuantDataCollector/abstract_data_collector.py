from abc import ABCMeta, abstractmethod
from QuantDataCollector.type import AdjustFlag, RequestFrequency, FilterType
from QuantDataCollector.data_collector_config import default_config

class DataCollectorError(Exception):
    """DataCollector专用异常"""
    pass

class AbstractDataCollector(metaclass=ABCMeta):
    @abstractmethod
    def __init__(self, config_dict = default_config):
        """构造函数

        在构造函数中，配置DataCollector的一些行为，比如是否使用cache，使用哪种类型的cache等

        Args:
          config: dict, 配置字典

        Raises:
          DataCollectorError: 配置项无法识别时
        """
        pass

    @abstractmethod
    def get_all_stock_code(self, day = None):
        """获取所有证券代码(包括股票、指数、可转债、ETF和其他)
        
        获取交易日day时，股市上所有证券代码，包括股票、指数、可转债、ETF和其他。

        Args:
          day: String，交易日，如果不是交易日，会导致失败。可省略，默认为离今天最近的交易日。

        Returns:
          Number: 错误码，0表示成功，否则表示失败，1表示非交易日
          list: 内容为表示证券代码的字符串

        Raises:
          DataCollectorError:
        """
        pass

    @abstractmethod
    def get_all_share_code(self, day = None):
        """获取所有股票代码
        
        获取交易日day时，股市上所有股票代码，不包括指数和其他。

        Args:
          day: String，交易日，如果不是交易日，会导致失败。可省略，默认为离今天最近的交易日。

        Returns:
          Number: 错误码，0表示成功，否则表示失败，1表示非交易日
          list: 内容为表示股票代码的字符串

        Raises:
          DataCollectorError:
        """
        pass

    @abstractmethod
    def get_stock_basic_data(self, stock_code_list = [], filter = FilterType.NoFilter):
        """获取某证券的基本信息

        通过list指定一组证券代码，获取对应证券的基本信息。主要包括：名称、上市日期、退市日期、证券类型、上市状态等

        Args:
          stock_code_list: list，一组证券代码，比如["sh.600000"]，传入空数组表示获取所有证券的基本信息
          filter：数据类型为FilterType，表示过滤方法，其中：
                   * NoFilter表示不过滤
                   * ShareFilter表示获取列表中的股票
                   * IndexFilter表示获取列表中的指数
                   * OtherFilter表示获取列表中的其他
                   * ConvertibleBondFilter表示获取列表中的可转债
                   * ETFFilter表示获取列表中的ETF
                 如果需要股票 + ETF,那么传入filter = ShareFilter | ETFFilter

        Returns:
          Number: 错误码，0表示获取成功
          list: list的每个元素为一个dict，dict的key如下：
                  * code: 证券代码
                  * code_name: 证券名称
                  * ipoDate：上市日期
                  * outDate: 退市日期
                  * type: 证券类型 其中1：股票，2：指数，3：其它，4：可转债，5：ETF
                  * status: 上市状态，其中1：上市，0：退市

        Raises:
          DataCollectorError
        """
        pass

    @abstractmethod
    def get_stock_type(self, stock_code):
        """获取证券类型

        获取code对应证券的类型

        Args:
          stock_code: String，证券代码，比如"sh.600000"

        Returns:
          Number: 错误码，0表示成功，否则表示失败
          String:
            '1'表示股票
            '2'表示指数
            '3'表示其他

        Raises:
          DataCollectorError:
        """
        pass

    @abstractmethod
    def get_stock_data_period(self, stock_code_list, start=None, end=None, frequency=RequestFrequency.DayK, adjust_flag =AdjustFlag.NoAdjust):
        """获取一组股票在某个交易日的数据
        功能、参数、返回值与Raise都与get_stock_data相同
        """
        pass

    @abstractmethod
    def get_stock_data(self, stock_code_list, day=None, frequency=RequestFrequency.DayK, adjust_flag=AdjustFlag.NoAdjust):
        """获取一组股票在某个交易日的数据
        
        获取股票代码在stock_code_list中的股票，在交易日day的数据，主要OHLC、成交量、成交额、换手率、市盈、市净、市销等
        
        Args:
          stock_code_list: list<String>，一组证券代码，比如["sh.600000"]
          day: 以字符串形式表示的日期，比如'2008-1-1'。默认为最新交易日
          frequency: 表示获取数据的k线类型，数据类型为RequestFrequency，具体含义如下
              * RequestFrequency.MonthK= 月K
              * RequestFrequency.WeekK = 周K
              * RequestFrequency.DayK = 日K
              * RequestFrequency.FiveMinutsK = 5分钟K
              * RequestFrequency.FifteenMinutsK = 15分钟K
              * RequestFrequency.ThirtyMinutsK = 30分钟K
              * RequestFrequency.HourK = 60分钟K
          adjust_flag：表示数据复权类型，数据类型为AdjustFlag，具体含义如下：
              * PostAdjust = 后复权
              * PreAdjust = 前复权
              * NoAdjust = 无复权
          
        Returns:
          Number: 错误码，0表示获取成功
          dict: key为股票代码，value为list，list中的每一项是一个dict，其中包含的key/value根据frequency有所不同：
                  * 周/月k: ["date", "code", "open", "high", "low", "close", "volume", "amount", "adjustflag", "turn", "pctChg"],
                  * 日k: ["date", "code", "open", "high", "low", "close", "preclose", "volume", "amount", "adjustflag", "turn", "tradestatus", "pctChg", "peTTM", "psTTM", "pcfNcfTTM", "pbMRQ","isST"]
                  * 分钟k: ["date", "time", "code", "open", "high", "low", "close", "volume", "amount", "adjustflag"]
                其中date -> 日期，code -> 证券码， open -> 开盘价
                  - date -> 表示数据对应日期，格式为YYYY-MM-DD
                  - time -> 表示数据对应的具体时间，格式为YYYYMMDDHHMMSSsss
                  - code -> 表示数据对应证券代码
                  - open -> 表示开盘价
                  - close -> 表示收盘价
                  - preclose -> 表示前收盘价
                  - high -> 表示最高价
                  - low -> 表示最低价
                  - volumn -> 表示成交量（累计 单位：股）
                  - amount -> 表示成交额（单位：人民币元）
                  - adjustflag -> 表示复权状态(1：后复权， 2：前复权，3：不复权
                  - turn -> 表示换手率
                  - tradestatus -> 表示交易状态(1：正常交易 0：停牌）
                  - pctChg -> 表示涨跌幅（百分比）：日涨跌幅=[(指定交易日的收盘价-指定交易日前收盘价)/指定交易日前收盘价]*100%
                  - peTTM -> 表示滚动市盈率：(指定交易日的股票收盘价/指定交易日的每股盈余TTM)=(指定交易日的股票收盘价*截至当日公司总股本)/归属母公司股东净利润TTM
                  - pbMRQ -> 表示市净率：(指定交易日的股票收盘价/指定交易日的每股净资产)=总市值/(最近披露的归属母公司股东的权益-其他权益工具)
                  - psTTM -> 表示市销率：(指定交易日的股票收盘价/指定交易日的每股销售额)=(指定交易日的股票收盘价*截至当日公司总股本)/营业总收入TTM
                  - pcfNcfTTM -> 表示市现率：(指定交易日的股票收盘价/指定交易日的每股现金流TTM)=(指定交易日的股票收盘价*截至当日公司总股本)/现金以及现金等价物净增加额TTM
                  - isST -> 表示是否ST股

        Raises:
          DataCollectorError:

        --------------------------------------------------------
        Override Notes:
          不限实现方式，为了性能，最好存储在数据库或者本地缓存
        """
        pass

    @abstractmethod
    def is_trade_day(self, day):
        """判断day是否为交易日
        
        Args:
          day: String，需要查询的日期，格式为:"2021-3-23"

        Returns:
          bool: 是否为交易日

        Raise:
          DataCollectorError
        """
        pass

    @abstractmethod
    def get_recent_trade_day(self, day=None):
        """获取day之前最接近day的交易日
        
        获取当前日期之前，最近的交易日期

        Args:
          day: String，日期，格式为："2022-1-20"。如果省略，则day为运行时日期

        Returns:
          String: 离day最近的交易日
        Raises:
        """
        pass
    @abstractmethod
    def get_data_collector_info(self):
        """获取关于数据收集器的一些信息，包括日志位置、数据来源等"""
        pass
