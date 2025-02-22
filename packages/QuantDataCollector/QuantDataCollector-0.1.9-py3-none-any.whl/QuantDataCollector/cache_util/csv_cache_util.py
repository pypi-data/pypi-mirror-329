
class CsvCacheUtil(AbstractCacheUtil):
    def __get_stock_data_from_csv_file(file_path):
        """从csv文件中读取股票数据
        
        从csv文件中读取股票数据
        
        Args:
          file_path: String，存储股票数据的csv文件的路径
          
        Returns:
          Numbers: 错误码，等于0时表示读取成功，否则表示读取失败
          pandas DataFrame: 读取成功时的股票数据
        """
        try:
            data = pd.read_csv(file_path)
        except:
            return 1, None
        
        return 0, data
    
    def __get_stock_data_by_code_from_csv_file(code, stock_type=None):
        """从csv文件中读取某只股票的数据

        通过指定股票代码，从csv中读取股票数据
        
        Args:
          code: String，证券代码，比如"sh.600000"
          stock_type: String，指定证券类型, '1'股票, '2'指数, '3'其他
          path: String，存储数据的csv文件
          
        Returns:
          Numbers: 错误码，等于0时表示读取成功，否则表示读取失败
          pandas DataFrame: 读取成功时的股票数据

        Raises:
          BaostockError:
            - 未登录
            - 获取证券基础信息失败
            - 证券类型错误
          IndexError: 获取的股票基础数据中，没有找到type对应的index
        """
        if(not stock_type):
            stock_type = self.get_stock_type(code)
        file_path = ""

        if(stock_type == STOCK_TYPE_SHARE):
            file_path += STOCK_DATA_SHARE_PATH
        elif(stock_type == STOCK_TYPE_INDEX):
            file_path += STOCK_DATA_INDEX_PATH
        elif(stock_type == STOCK_TYPE_OTHER):
            file_path += STOCK_DATA_OTHER_PATH
