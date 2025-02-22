# 数据收集

## 简介

> QuantDataCollector的目的是提供统一、稳定的数据接口，用户可以不用考虑数据获取问题，专注策略开发。

QuantDataCollector从各种数据源收集相关数据，并且可以选择缓存在本地，目前的覆盖的数据及数据源包括：

- baostock: Python库，提供股市、债券、货币、存款等数据。



## 使用

通过DataCollector类向外提供统一接口，以获取所有股票sz.399995的基本信息为例：

```python
import QuantDataCollector as qdc
from QuantDataCollector import RequestFrequency, AdjustFlag

data_collector = qdc()
error_code, data = data_collector.get_stock_data(["sz.399990", "sh.600000"],"2024-8-6",RequestFrequency.DayK, AdjustFlag.NoAdjust)
print(data)
```

也可以对`data_collector`进行配置：

```python
from QuantDataCollector import cache_config, log_config
from QuantDataCollector import RequestFrequency, AdjustFlag
import QuantDataCollector as qdc

data_collector = qdc({"cache" : cache_config.NO_CACHE, "log": log_config.DEBUG_LOG})
error_code, data = data_collector.get_stock_data(["sz.399990", "sh.600000"],"2024-8-6",RequestFrequency.DayK, AdjustFlag.NoAdjust)
print(data)
```
结果：

> {'sh.600000': [{'date': '2022-01-20', 'code': 'sh.600000', 'adjust_flag': 2, 'time': '09:35:00.000', 'open': 7.5725, 'high': 7.61622, 'low': 7.55501, 'close': 7.58999, 'volume': 3313587, 'amount': 28750200.0},**...***,{'date': '2022-01-20', 'code': 'sh.600000', 'adjust_flag': 2, 'time': '15:00:00.000', 'open': 7.68618, 'high': 7.71241, 'low': 7.67743, 'close': 7.69492, 'volume': 14931802, 'amount': 131355000.0}], 'sh.688393': [{'date': '2022-01-20', 'code': 'sh.688393', 'adjust_flag': 2, 'time': '09:35:00.000', 'open': 30.7454, 'high': 30.8524, 'low': 30.58, 'close': 30.7259, 'volume': 42037, 'amount': 1328890.0},**...**, {'date': '2022-01-20', 'code': 'sh.688393', 'adjust_flag': 2, 'time': '15:00:00.000', 'open': 29.967, 'high': 30.0059, 'low': 29.9573, 'close': 29.9573, 'volume': 16547, 'amount': 509588.0}], 'sh.688315': [{'date': '2022-01-20', 'code': 'sh.688315', 'adjust_flag': 2, 'time': '09:35:00.000', 'open': 39.1305, 'high': 39.3191, 'low': 38.525, 'close': 38.793, 'volume': 26229, 'amount': 1022700.0},**...**,{'date': '2022-01-20', 'code': 'sh.688315', 'adjust_flag': 2, 'time': '15:00:00.000', 'open': 35.3386, 'high': 35.3386, 'low': 35.279, 'close': 35.3187, 'volume': 75175, 'amount': 2674400.0}]}




### 获取basic data

```python
from QuantDataCollector import cache_config, log_config
from QuantDataCollector import RequestFrequency, AdjustFlag, FilterType
import QuantDataCollector as qdc

data_collector = qdc({"cache" : cache_config.NO_CACHE, "log": log_config.DEBUG_LOG})
error_code, data = data_collector.get_stock_basic_data([], FilterType.ETFFilter) # 获取所有ETF的basic data
print(data)
```



### 日志查看

通过`get_data_collector_info`接口查看日志路径，进而查看日志

```python
import QuantDataCollector as qdc

data_collector = qdc()
print(data_collector.get_data_collector_info())
```



### API接口

* get_all_share_code(day)
    > **获取所有股票代码**
    > 
    > 获取交易日day时，股市上所有股票代码，不包括指数和其他。
    > 
    > PS:
    >    * 如果day为最新交易日，交易结束前获取结果为空
    >    * **目前的实现速度比较慢，谨慎使用**
    > 
    > Args:
    > * day: String，交易日，如果不是交易日，会导致失败。可省略，默认为离今天最近的交易日。
    > 
    > Returns:
    > * Number: 错误码，0表示成功，否则表示失败，1表示非交易日
    > * List: 内容为表示股票代码的字符串
    > 
    > Raises:
    > * DataCollectorError:

* get_all_stock_code(day)
    > **获取所有证券代码(包括股票、指数、可转债、ETF和其他)**
    > 
    > 获取交易日day时，股市上所有证券代码，包括股票、指数、可转债、ETF和其他。
    > 
    > PS: 如果day为最新交易日，交易结束前获取结果为空
    > 
    > Args:
    > * day: String，交易日，如果不是交易日，会导致失败。可省略，默认为离今天最近的交易日。
    > 
    > Returns:
    > * Number: 错误码，0表示成功，否则表示失败，1表示非交易日
    > * List: 内容为表示证券代码的字符串
    > 
    > Raises:
    > * DataCollectorError:

* get_data_collector_info()
    > **获取关于数据收集器的一些信息，包括日志位置、数据来源等**

* get_recent_trade_day(day)
    > **获取day之前最接近day的交易日**
    > 
    > 获取当前日期之前，最近的交易日期
    > 
    > Args:
    > * day: String，日期，格式为："2022-1-20"。如果省略，则day为运行时日期
    > 
    > Returns:
    > * String: 离day最近的交易日
    > Raises:

* get_stock_basic_data(stock_code_list, filter):
    > **获取某证券的基本信息**
    > 
    > 通过list指定一组证券代码，获取对应证券的基本信息。主要包括：名称、上市日期、退市日期、证券类型、上市状态等
    > 
    > Args:
    > * stock_code_list: list，一组证券代码，比如["sh.600000"]，**传入空数组表示获取所有证券的基本信息**
    > * filter：数据类型为FilterType，表示过滤方法，其中：
    >    * NoFilter表示不过滤
    >    * ShareFilter表示获取列表中的股票
    >    * IndexFilter表示获取列表中的指数
    >    * OtherFilter表示获取列表中的其他
    >    * ConvertibleBondFilter表示获取列表中的可转债
    >    * ETFFilter表示获取列表中的ETF
    >    * NotDelisted表示要求未退市，也就是过滤掉已退市股票
    >          如果需要股票 + ETF,那么传入filter = ShareFilter | ETFFilter
    >
    > PS: 由于Cache现阶段还在收集数据，如果stock_code_list很长，本函数会花费较多时间。如果想要针对所有股票，建议传空数组[]，如：get_stock_basic_data([],FilterType.NotDelisted)
    > 
    > Returns:
    > * Number: 错误码，0表示获取成功
    > * List: list的每个元素为一个dict，dict的key如下：
    >   * code: 证券代码
    >   * code_name: 证券名称
    >   * ipoDate：上市日期
    >   * outDate: 退市日期
    >   * type: 证券类型 其中1：股票，2：指数，3：其它，4：可转债，5：ETF
    >   * status: 上市状态，其中1：上市，0：退市
    > 
    > Raises:
    >  * DataCollectorError

* get_stock_data(stock_code_list, day, frequency, adjust_flag)
    > **获取一组股票在某个交易日的数据**
    > 
    > 获取股票代码在stock_code_list中的股票，在交易日day的数据
    > 
    > Args:
    > * stock_code_list: list<String>，一组证券代码，比如["sh.600000"]
    > * day: 以字符串形式表示的日期，比如'2008-1-1'。默认为最新交易日
    > * frequency: 表示获取数据的k线类型，数据类型为RequestFrequency，具体含义如下
    >   * RequestFrequency.MonthK= 月K
    >   * RequestFrequency.WeekK = 周K
    >   * RequestFrequency.DayK = 日K
    >   * RequestFrequency.FiveMinutsK = 5分钟K
    >   * RequestFrequency.FifteenMinutsK = 15分钟K
    >   * RequestFrequency.ThirtyMinutsK = 30分钟K
    >   * RequestFrequency.HourK = 60分钟K

    > * adust_flag：表示数据复权类型，数据类型为AdjustFlag，具体含义如下：
    >   * PostAdjust = 后复权
    >   * PreAdjust = 前复权
    >   * NoAdjust = 无复权
    >   
    > Returns:
    >  * Number: 错误码，0表示获取成功
    >  * Dict: key为股票代码，value为list。list中的每一项是一个dict，其中包含的key/value根据frequency有所不同：
    >     * 周/月k: ["date", "code", "open", "high", "low", "close", "volume", "amount", "adjustflag", "turn", "pctChg"],
    >     * 日k: ["date", "code", "open", "high", "low", "close", "preclose", "volume", "amount", "adjustflag", "turn", "tradestatus", "pctChg", "peTTM", "psTTM", "pcfNcfTTM", "pbMRQ","isST"]
    >     * 分钟k: ["date", "time", "code", "open", "high", "low", "close", "volume", "amount", "adjustflag"]
    >        - date -> 表示数据对应日期，格式为YYYY-MM-DD
    >        - time -> 表示数据对应的具体时间，格式为YYYYMMDDHHMMSSsss
    >        - code -> 表示数据对应证券代码
    >        - open -> 表示开盘价
    >        - close -> 表示收盘价
    >        - preclose -> 表示前收盘价
    >        - high -> 表示最高价
    >        - low -> 表示最低价
    >        - volumn -> 表示成交量（累计 单位：股）
    >        - amount -> 表示成交额（单位：人民币元）
    >        - adjustflag -> 表示复权状态(1：后复权， 2：前复权，3：不复权
    >        - turn -> 表示换手率
    >        - tradestatus -> 表示交易状态(1：正常交易 0：停牌）
    >        - pctChg -> 表示涨跌幅（百分比）：日涨跌幅=[(指定交易日的收盘价-指定交易日前收盘价)/指定交易日前收盘价]*100%
    >        - peTTM -> 表示滚动市盈率：(指定交易日的股票收盘价/指定交易日的每股盈余TTM)=(指定交易日的股票收盘价*截至当日公司总股本)/归属母公司股东净利润TTM
    >        - pbMRQ -> 表示市净率：(指定交易日的股票收盘价/指定交易日的每股净资产)=总市值/(最近披露的归属母公司股东的权益-其他权益工具)
    >        - psTTM -> 表示市销率：(指定交易日的股票收盘价/指定交易日的每股销售额)=(指定交易日的股票收盘价*截至当日公司总股本)/营业总收入TTM
    >        - pcfNcfTTM -> 表示市现率：(指定交易日的股票收盘价/指定交易日的每股现金流TTM)=(指定交易日的股票收盘价*截至当日公司总股本)/现金以及现金等价物净增加额TTM
    >        - isST -> 表示是否ST股
    > 
    > Raises:
    > * DataCollectorError:

* get_stock_data_period(stock_code_list, start, end, frequency, adjust_flag)
    > **获取一组股票在某个交易日的数据**
    > 功能、参数、返回值与Raise都与get_stock_data相同

* tock_type(stock_code)
    > **获取证券类型**
    > 
    > 获取code对应证券的类型
    > 
    > Args:
    > * stock_code: String，证券代码，比如"sh.600000"
    > 
    > Returns:
    > * Number: 错误码，0表示成功，否则表示失败
    > * String:
    >   * '1'表示股票
    >   * '2'表示指数
    >   * '3'表示其他
    > 
    > Raises:
    > * DataCollectorError:

* is_trade_day(day)
    > **判断day是否为交易日**
    > 
    > Args:
    > * day: String，需要查询的日期，格式为:"2021-3-23"
    > 
    > Returns:
    > * bool: 是否为交易日
    > 
    > Raise:
    > * DataCollectorError


## 如何设置MySQL

目前仅支持MySQL作为缓存，为了使用缓存，需要设置环境变量：

* MYSQL_HOST: MySQL服务器地址
* MYSQL_USER: MySQL用户名
* MYSQL_PASSWORD: MySQL密码

环境变量设置方法

* Windows
    `setx MYSQL_HOST 192.168.71.17`
    想要环境变量生效需要重启terminal，如果使用anaconda，则需要重启anaconda才能生效，如果使用vscode的terminal，也需要重启vscode

* Linux / MacOS
    相比Windows要简单一些，只需要`export MYSQL_HOST=192.168.6.19`即可


## 架构

为了提供统一的接口，QuantDataCollector包采用了**工厂方法**。

对于不同的数据源，实现时都要继承`abstract_data_collector.py`中的`AbstractDataCollector`类，最终由`data_collector.py`提供统一接口。

详见：[架构](../../documentations/DataCollectorDocs/DataCollectorStructure.md)

## 数据源及其特点


### baostock

已经包装好的**股票数据拉取**Python库，数据覆盖

- 股票
- 公司业绩
- 货币
- 存款利率

优点：

- 使用简单

缺点：

- 服务由他人提供，已有收费趋势，可用性不高
