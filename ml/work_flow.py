import logging
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
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(lineno)d: %(message)s')
logger = logging.getLogger(__name__)


def execute():
    """
    执行主函数
    """
    # 1.读取配置
    config = read_config()
    conn = conn_engine(config['flask']['SQLALCHEMY_DATABASE_URI'])

    # 2.读入数据
    data_source = get_data_source()
    data_type = data_source['type']
    data_uri = data_source['uri']
    samples = read_data(data_type, data_uri)

    # 3.特征工程
    data_features = get_data_feature()
    for f in data_features:
        logger.debug(f)
        samples = extract_feature(samples, f)

    # 4.加载模型
    model_pubs = get_model_pub()
    models = load_models(model_pubs)

    # 5.预测结果
    results = model_predict(models, samples)
    model_outputs = get_model_output()
    save_results(model_outputs, results)

    return 1

