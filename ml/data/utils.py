import sqlalchemy
import pandas as pd
from types import FunctionType
from models.data_source import DataSource
from models.data_table import DataTable
from models.data_feature import DataFeature
from sqlalchemy.sql import text,and_,or_,func

"""
数据处理工具包
1.读取数据源配置
2.读入数据
3.特征工程
"""
conn_engine = None


def create_connect(data_uri):
    """
    建立连接
    :param data_uri:
    :return:
    """
    global conn_engine
    if conn_engine is None:
        conn_engine = sqlalchemy.create_engine(data_uri, echo=True)
    return conn_engine


def get_data_source():
    """
    获取数据源
    """
    data_source = DataSource()
    sql_data_source = """1=1"""
    res = data_source.query.filter(text(sql_data_source)).order_by(text("id desc")).limit(1).all()
    return res[0]


def get_data_table(dt_id):
    """
    获取数据表
    :param dt_id:
    """
    data_table = DataTable()
    ret = None
    if dt_id is not None:
        sql_data_table = "id=" + str(dt_id)
        res = data_table.query.filter(text(sql_data_table)).limit(1).all()
        ret = res[0]
    return ret


def read_data(data_type, data_uri, batch_size=20):
    """
    读取数据
    :param data_type:
    :param data_uri:
    :param batch_size:
    :return:
    """
    sample_data = None
    if data_type == 'csv':
        sample_data = pd.read_csv(data_uri, nrows=batch_size)
    return sample_data


def get_data(dt_id, nrows=10):
    """
    取得预览数据
    :param dt_id: 数据表编号
    :param nrows: 读取行数
    """
    ds_conf = get_data_source()
    dt_conf = get_data_table(dt_id)
    data_type = ds_conf.type
    data_uri = ds_conf.uri
    if data_type == 'csv':
        data_uri += dt_conf.type + '.csv'
    df = read_data(data_type, data_uri, nrows)
    return df


def get_data_feature():
    """
    获取特征工程配置
    """
    data_feature = DataFeature()
    sql_data_feature = """1=1"""
    res = data_feature.query.filter(text(sql_data_feature)).order_by(text("id desc")).all()
    return res


def parse_rules(rule_type, rules):
    """
    todo 特征规则解析
    :param rule_type:
    :param rules:
    :return: 返回一个可执行的方法用于处理数据
    """
    rule_func = None
    if rules is not None:
        # 注意，这里的str描述函数体时，前面不能有多余空格
        func_body = """
def rules(df):
    print(df.head)
    return df
        """
        rule_code = compile(func_body, "<df>", "exec")
        rule_func = FunctionType(rule_code.co_consts[0], globals(), "rules")
    return rule_func


def extract_feature(df, rule_func):
    """
    todo 特征抽取
    :param df:
    :param rule_func:
    :return:
    """
    if rule_func is not None:
        df_result = rule_func(df)
    return df_result


def preview_data_feature(df_id):
    """
    特征预览
    :param df_id: 特征规则编号
    """
    data_feature = DataFeature()
    sql_data_feature = "id=" + str(df_id)
    res = data_feature.query.filter(text(sql_data_feature)).limit(1).all()
    df_conf = res[0]
    df_data = get_data(df_conf.dt_id, nrows=10)
    df_rules = parse_rules(df_conf.rule_type, df_conf.rules)
    df_result = extract_feature(df_data, df_rules)
    return df_result

