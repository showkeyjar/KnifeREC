from ml.data.utils import *
"""
系统主工作流程
"""


def read_config():

    return None


def execute():
    config = read_config()
    samples = read_data(config['data_type'], config['data_uri'])
    pass
