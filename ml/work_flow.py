from tools.utils import *
from ml.data.utils import *
"""
系统主工作流程

1.读取配置
2.读入数据
3.特征工程
4.模型训练
5.模型部署
6.模型监控
"""


def execute():
    config = read_config()
    samples = read_data(config['data_type'], config['data_uri'])
    pass
