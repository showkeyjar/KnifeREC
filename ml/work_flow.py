from tools.utils import *
from ml.data.utils import *
from ml.model.utils import *
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
    # 1.读取配置
    config = read_config()
    conn = conn_engine(config['flask']['SQLALCHEMY_DATABASE_URI'])
    # 2.读入数据
    data_source = get_data_source()
    data_type = data_source['type']
    data_uri = data_source['uri']
    samples = read_data(data_type, data_uri)
    # todo 3.特征工程
    return 1

