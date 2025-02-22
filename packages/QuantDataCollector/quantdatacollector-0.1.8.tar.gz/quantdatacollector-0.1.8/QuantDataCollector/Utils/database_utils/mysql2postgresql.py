import os
import re
from QuantDataCollector.Utils.database_utils.mysql_utils import mysqlOps
from QuantDataCollector.Utils.database_utils.postgresql_utils import postgresqlOps
from datetime import date

"""
一开始数据放在mysql，后来换了postgresql，所以实现了这个类完成数据的迁移。
但是目前只实现了两个功能：
- 复制表格（不包括数据）
- 复制表格数据

两者都存在一些问题
比如目前无法迁移外键等
后者则是比较慢，一千五百万条数据迁移了将近3天，甚至低于从网上下载数据
"""


class mysql2postgresql:
    """
    将数据从mysql转移到postgresql
    """
    
    def __init__(self,
                 mysql_host=os.getenv('MYSQL_HOST'),
                 mysql_user=os.getenv('MYSQL_USER'),
                 mysql_password=os.getenv('MYSQL_PASSWORD'),
                 mysql_database=None,
                 mysql_port=3306,
                 postgresql_host=os.getenv('POSTGRESQL_HOST'),
                 postgresql_user=os.getenv('POSTGRESQL_USER'),
                 postgresql_password=os.getenv('POSTGRESQL_PASSWORD'),
                 postgresql_database=os.getenv('POSTGRESQL_DATABASE'),
                 postgresql_port=3306):
        self.mysql_ops = mysqlOps(mysql_host,mysql_user,mysql_password,mysql_database,mysql_port)
        self.postgresql_ops = postgresqlOps(postgresql_host,postgresql_user,postgresql_password,postgresql_database,postgresql_port)


    def copy_table_skeleton(self,table_name):
        """
        拷贝表格结构，但不拷贝表格内容
        """
        sql = "SHOW CREATE TABLE " + table_name
        mysql_create_cmd = self.mysql_ops.excute_cmd(sql)[0][1]
        mysql_create_cmd = mysql_create_cmd.replace('`', '') #删除字符`
        mysql_create_cmd_lines = mysql_create_cmd.split('\n')
        mysql_create_cmd_lines = mysql_create_cmd_lines[:-1]
        line_num = len(mysql_create_cmd_lines)
        postgresql_create_cmd = "" + mysql_create_cmd_lines[0]
        print(mysql_create_cmd_lines)
        print("\n")
        for i in range(1, line_num):
            if "PRIMARY KEY" in mysql_create_cmd_lines[i]:
                postgresql_create_cmd += mysql_create_cmd_lines[i][:-1] #不要最后的逗号（没有逗号会出错）
                continue
            elif "FOREIGN KEY" in mysql_create_cmd_lines[i]:
                #postgresql_create_cmd += mysql_create_cmd_lines[i]
                continue

            cmd_words = re.split(',| ', mysql_create_cmd_lines[i])
            postgresql_create_cmd += cmd_words[2] + " "
            postgresql_create_cmd += cmd_words[3] + " "
            words_num = len(cmd_words)
            j = 4
            while j < words_num:
                if cmd_words[j] == "NOT":
                    # 处理 NOT NULL情况
                    # type int NOT NULL DEFAULT '1'
                    postgresql_create_cmd += cmd_words[j] + " " + cmd_words[j+1] + " "
                    j += 1
                elif cmd_words[j] == "DEFAULT":
                    # 处理DEFAULT
                    # status int DEFAULT '1'
                    postgresql_create_cmd += cmd_words[j] + " " + cmd_words[j+1] + " "
                    j += 1
                elif cmd_words[j] == "NULL":
                    # 可能出现NULL的情况
                    # NOT NULL
                    # DEFAULT NULL
                    continue
                elif cmd_words[j] == "COMMENT":
                    #postgresql_create_cmd += cmd_words[j] + " " + cmd_words[j+1] + " "
                    j += 1
                # else: # 其他情况暂时忽略
                j += 1
            postgresql_create_cmd += ","

        postgresql_create_cmd += " )"

        postgresql_create_cmd = re.sub("tinyint\(*[0-9]*\)*","smallint", postgresql_create_cmd) # postgresql 中没有tinyint，可以等效替换为smallint，且没有展示宽度的设置，所以将tinyint(1) 也会变为smallint
        postgresql_create_cmd = re.sub("double\(*[0-9]*\)*","double precision", postgresql_create_cmd) # postgresql 中没有double，可以等效替换为double precision
        postgresql_create_cmd = re.sub("float\(*[0-9]*\)*","real", postgresql_create_cmd) # postgresql 中没有float，可以等效替换为real
        print(postgresql_create_cmd)

        res = self.postgresql_ops.excute_cmd(postgresql_create_cmd)
        return res

    def copy_table(self,table_name, step = 10000):
        """
        假设mysql和postgresql中都存在table_name，且结构相同，将前者数据追加到后者
        step表示每次迁移的数据条数，一起迁移全部数据是不明智的，不仅占用内存多，而且很可能中间出错
        """
        res = self.mysql_ops.data_num(table_name)
        data_num = 0
        if res[0]:
            data_num = int(res[1])
        offset = 0
        columns = self.postgresql_ops.get_table_columns(table_name)
        column_num = len(columns)
        while offset < data_num:
            res = self.mysql_ops.query(table_name = table_name, limit = step, offset = offset)
            if res[0]:
                for data in res[1]:
                    data_dict = {}
                    for i in range(column_num):
                        if data[i]:
                            if isinstance(data[i], date):
                                data_dict[columns[i]] = data[i].strftime('%Y-%m-%d')
                            else:
                                data_dict[columns[i]] = data[i]
                    res, msg = self.postgresql_ops.insert(table_name, data_dict)
                    if not res:
                        # 插入失败
                        print(msg)

            offset += step




if __name__ == "__main__":
    my2postgre = mysql2postgresql(mysql_database = "stock_data", postgresql_database = "postgres")
    #print(my2postgre.copy_table_skeleton("stock_daily_data"))
    #print(my2postgre.copy_table_skeleton("stock_basic_data"))
    
    #my2postgre.copy_table("stock_basic_data")
    my2postgre.copy_table("stock_daily_data")
