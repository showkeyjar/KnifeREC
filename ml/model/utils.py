
"""
todo 模型工具包

4.模型训练
5.模型部署
"""


def train_model(model, data):
    """
    模型训练
    :param model:
    :param data:
    :return:
    """
    try:
        model.train(data)
    except:
        pass
    return True


def pub_model(model,conf):
    """
    模型部署
    :param model:
    :param conf:
    :return:
    """
    pass
