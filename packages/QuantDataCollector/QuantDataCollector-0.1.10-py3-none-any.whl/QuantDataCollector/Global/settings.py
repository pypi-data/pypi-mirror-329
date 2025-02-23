"""
全局使用的静态变量

包括运行结果、日志所在路径等
"""

from enum import IntEnum, unique
import sys
import os
import logging

# -------------- 私有方法 ---------------
def get_parent_path(path, level=1):
    """获取父路径
    
    由于不同的系统中，获取父路径的方式不同，利用os的接口实现

    Args:
      path: String，当前路径
      level: Number，父路径的级别，比如level=2，相当于linux中的path/../../

    Returns:
      String: 父路径
    """
    res_path = path
    for i in range(level):
        res_path = os.path.split(res_path)[0]
    return res_path

REPO_ROOT_PATH=get_parent_path(os.path.abspath(__file__),2)
RESULTS_ROOT_PATH=REPO_ROOT_PATH + "/results"

# ------------- 日志相关配置 -----------
LOGGING_LEVEL=logging.DEBUG
LOGGING_FILE_DIR=RESULTS_ROOT_PATH + "/log"
LOGGING_FILE_NAME=LOGGING_FILE_DIR + "/log.txt"

# ------------- 数据库相关 --------------

MYSQL_STOCK_DATABASE_NAME="stock_data"
MYSQL_STOCK_BAISC_DATA_TABLE_NAME="stock_basic_data"
MYSQL_STOCK_MINUTE_K_DATA_TABLE_NAME="stock_k_data_minute"
MYSQL_STOCK_DAY_K_DATA_TABLE_NAME="stock_k_data_day"
MYSQL_STOCK_WEEK_K_DATA_TABLE_NAME="stock_k_data_week"
MYSQL_STOCK_MONTH_K_DATA_TABLE_NAME="stock_k_data_month"
