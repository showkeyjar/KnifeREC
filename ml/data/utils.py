import pandas as pd

"""
数据处理工具包
"""


def read_data(data_type,data_uri):
    """
    读取数据
    """
    sample_data = None
    if data_type == 'csv':
        sample_data = pd.read_csv(data_uri)
    return sample_data

