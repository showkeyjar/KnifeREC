import sqlalchemy
import pandas as pd

"""
数据处理工具包
"""


def create_connect():
    sqlalchemy.create_engine("sqlite:///test.db?check_same_thread=False", echo=True)


def read_data(data_type,data_uri):
    """
    读取数据
    """
    sample_data = None
    if data_type == 'csv':
        sample_data = pd.read_csv(data_uri)
    return sample_data


def extract_feature(df, columns):
    """
    特征抽取
    """
    df_result = df[columns]
    return df_result
