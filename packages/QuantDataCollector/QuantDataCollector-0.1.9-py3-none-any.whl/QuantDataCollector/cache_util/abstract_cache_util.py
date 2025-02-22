from abc import ABCMeta, abstractmethod
from QuantDataCollector.cache_util.cache_util_config import default_config

class CacheUtilError(Exception):
    """缓存工具专用异常"""
    pass

class AbstractCacheUtil(metaclass=ABCMeta):
    @abstractmethod
    def __init__(self, config_dict = default_config):
        """构造函数

        在构造函数中，配置CacheUtil的一些行为，比如日志等级

        Args:
          config: dict, 配置字典
        """
        pass

    @abstractmethod
    def has_stock_basic_cache(self, stock_code):
        """某支股票的基本信息是否有缓存

        指定股票代码，查询该股票基本信息是否已经在缓存中

        Args:
          stock_code: String，股票代码，比如"sh.600000"

        Returns:
          bool: 存在缓存返回True，否则返回False

        Raises:
          CacheUtilError
        """
        pass

    @abstractmethod
    def get_stock_basic_data(self, stock_code):
        """从缓存中读取某支股票的基本信息

        指定股票代码，从缓存中读取其基本信息。如果没有缓存，会返回空字典

        Args:
          stock_code: String，股票代码，比如"sh.600000"

        Returns:
          dict: 股票基本数据字典，格式为{"code_name":"上证50", "ipoDate":"1999-1-1", ...}

        Raises:
          CacheUtilError
        """
        pass

    @abstractmethod
    def has_stock_cache(self, stock_code, date, frequency = 'd', adjust_flag = 2):
        """判断某只股票某天的数据是否有缓存

        根据股票代码和日期，判断某支股票该日期的数据是否有缓存

        Args:
          stock_code: String，股票代码，比如"sz.399995"
          date: String，格式为YYYY-MM-DD的日期
          frequency: String，表示请求的k线类型
                     默认为d，日k线；d=日k线、w=周、m=月、5=5分钟、15=15分钟、30=30分钟、60=60分钟
          adjust_flag: Number, 复权方式，默认前复权。 1 后复权，2 前复权，3 不复权

        Returns:
          bool:有缓存返回True

        Raises:
          CacheUtilError
        """
        pass

    @abstractmethod
    def get_stock_data(self, stock_code, date, frequency = 'd', adjust_flag = 2):
        """从缓存中获取某只股票某天的数据

        根据股票代码和日期，获取缓存中某支股票该日期的数据

        Args:
          stock_code: String，股票代码，比如"sz.399995"
          date: String，格式为YYYY-MM-DD的日期
          frequency: String，表示请求的k线类型
                     默认为d，日k线；d=日k线、w=周、m=月、5=5分钟、15=15分钟、30=30分钟、60=60分钟
          adjust_flag: Number, 复权方式，默认前复权。 1 后复权，2 前复权，3 不复权

        Returns:
          dict: 
        """
        pass

    @abstractmethod
    def has_batch_cache(self, stock_code, start, end, frequency = 'd', adjust_flag = 2):
        """判断某支股票某个时间段内的数据是否有缓存

        通过指定股票代码是时间段，判断该股票该时间段内的数据是否有缓存。如果任一日期内的数据没有缓存，就视为没有缓存

        Args:
          stock_code: String，股票代码，比如"sz.399995"
          start: String，格式为YYYY-MM-DD的日期
          end: String，格式为YYYY-MM-DD的日期
          frequency: String，表示请求的k线类型
                     默认为d，日k线；d=日k线、w=周、m=月、5=5分钟、15=15分钟、30=30分钟、60=60分钟
          adjust_flag: Number, 复权方式，默认前复权。 1 后复权，2 前复权，3 不复权

        Returns:
          bool:

        """
        pass

    @abstractmethod
    def get_stock_data_batch(self, stock_code, start, end, frequency = 'd', adjust_flag = 2):
        """获取某支股票某个时间段内的数据

        通过指定股票代码是时间段，从缓存中获取该股票该时间段内的数据。返回字典中，以每个日期会key，对应响应日期的数据。（极端情况下，可能缺失某些日期数据)

        Args:
          stock_code: String，股票代码，比如"sz.399995"
          start: String，格式为YYYY-MM-DD的日期
          end: String，格式为YYYY-MM-DD的日期
          frequency: String，表示请求的k线类型
                     默认为d，日k线；d=日k线、w=周、m=月、5=5分钟、15=15分钟、30=30分钟、60=60分钟
          adjust_flag: Number, 复权方式，默认前复权。 1 后复权，2 前复权，3 不复权

        Returns:
          Dict: 字典，以日期为key，对应该日期的数据
        """
        pass

    @abstractmethod
    def save_stock_data(self, stock_code, date, data, frequency):
        """保存某股票某天的数据

        将指定股票某天的数据保存到缓存

        Args:
          stock_code: String，股票代码
          data: dict，数据index及其数值
          frequency: String，表示要保存的k线类型
                     默认为d，日k线；d=日k线、w=周、m=月、5=5分钟、15=15分钟、30=30分钟、60=60分钟

        Returns:
          bool: 保存成功返回True
        """
        pass

    @abstractmethod
    def save_stock_basic_data(self, stock_code, data):
        """保存证券基本信息

        保存某证券的基本信息到缓存中

        Args:
          stock_code: String，股票代码
          data: Dictionary，数据index及其数值

        Returns:
          bool: 保存成功返回True
        """
        pass

    @abstractmethod
    def delete_stock_basic_data(self, stock_code):
        """删除基本信息缓存

        删除某证券的基础信息缓存

        Args:
          stock_code: String, 股票代码
        
        Returns:
          bool: 删除是否成功，如果缓存不存在，或者删除失败，返回False
        """
        pass

    @abstractmethod
    def delete_stock_data(self, stock_code, date, frequency, adjust_flag):
        """删除股票信息缓存

        删除某证券的信息缓存

        Args:
          stock_code: String, 股票代码，设为None则删除所有数据（危险）
          date: Date希望删除的日期，如果指定为None则删除所有日期数据
          frequency: String，表示要删除的k线类型
                     d=日k线、w=周、m=月、5=5分钟、15=15分钟、30=30分钟、60=60分钟
                     指定为None表示删除所有frequency的数据
          adjust_flag: Number, 复权方式，默认前复权。 1 后复权，2 前复权，3 不复权
                      指定为None表示删除所有复权方式的数据
          
        
        Returns:
          bool: 删除是否成功，如果缓存不存在，或者删除失败，返回False
        """
        pass

    @abstractmethod
    def clear_basic_cache(self):
        """清空股票基本信息缓存"""
        pass

    @abstractmethod
    def clear_full_cache(self):
        """清空股票信息缓存"""
        pass

    @abstractmethod
    def cache_info(self):
        """返回关于缓存的一些信息，比如存储方式，存储位置等"""
        pass
