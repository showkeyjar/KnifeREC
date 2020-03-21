import sqlalchemy
import pandas as pd

"""
数据处理工具包

2.读入数据
3.特征工程
"""


def create_connect():
    """
    建立连接
    :return:
    """
    sqlalchemy.create_engine("sqlite:///test.db?check_same_thread=False", echo=True)


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


def extract_feature(df, columns):
    """
    特征抽取
    :param df:
    :param columns:
    :return:
    """
    df_result = df[columns]
    return df_result

