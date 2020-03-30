import sqlalchemy
import pandas as pd
from models.data_source import DataSource
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
    sql_data_source = """
        select * from data_source limit 1
        """
    res = data_source.query.filter(text(sql_data_source)).order_by(text("id desc")).limit(1).all()
    return res[0]


def read_data(data_type,data_uri):
    """
    读取数据
    :param data_type:
    :param data_uri:
    :return:
    """
    sample_data = None
    if data_type == 'csv':
        sample_data = pd.read_csv(data_uri)
    return sample_data


def get_data_feature():
    """
    获取特征工程配置
    """
    data_feature = DataFeature()
    sql_data_feature = """
        select * from data_feature limit 100
        """
    res = data_feature.query.filter(text(sql_data_feature)).order_by(text("id desc")).all()
    return res


def extract_feature(df, rules):
    """
    todo 特征抽取
    :param df:
    :param rules:
    :return:
    """
    rule_type = rules['rule_type']
    if rule_type == 'filter':
        df_result = df
    return df_result

