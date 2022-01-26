import dill
from models.model_pub import ModelPub
from models.model_output import ModelOutput
from sqlalchemy.sql import text,and_,or_,func
from ml.data.utils import get_train_data
from ml.model.sort import *
"""
todo 模型工具包

4.模型训练
5.模型部署
"""

class PredictAI():
    type = None

    def __init__(self, type=None) -> None:
        self.type = type

    def get_model(self, type='sort'):
        """
        取得模型
        """
        # model_func = exec(type)
        model_func = getattr(type, "load")
        return model_func

    def train_model(self, model, data):
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

    def pub_model(self, model, conf):
        """
        todo 模型部署
        :param model:
        :param conf:
        :return:
        """
        pass


    def get_model_pub(self):
        """
        取得部署的模型
        """
        model_pub = ModelPub()
        sql_model_pub = """
                select * from model_pub limit 100
                """
        res = model_pub.query.filter(text(sql_model_pub)).order_by(text("id desc")).all()
        return res


    def load_models(self, pub_models):
        """
        加载模型
        :param pub_models:
        """
        models = []
        for pm in pub_models:
            model_path = 'data/model/' + pm + '.pkl'
            try:
                with open(model_path, 'rb') as f:
                    model = dill.load(f)
            except:
                model = None
            if model is not None:
                models.append(model)
        return models


    def model_predict(self, models, df):
        """
        预测结果
        :param models:
        :param df:
        """
        results = []
        for m in models:
            result = m.predict(df)
            results.append(result)
        return results


    def get_model_output(self, type=None):
        if type is None:
            type = self.type
        model_output = ModelOutput()
        sql_model_output = """
                select * from model_output where model={type} limit 100
                """
        res = model_output.query.filter(text(sql_model_output)).order_by(text("id desc")).all()
        return res


    def save_results(self, model_output, df):
        """
        保存结果
        :param model_output:
        :param df:
        """
        model_output.save(df)


    def load_one_model(self, mid):
        """
        todo 加载模型
        :param mid:
        """
        # 这里不能直接使用 get_model
        model = self.get_model(mid)
        return model


    def start_train_model(self, mid, dt_id):
        """
        训练模型
        :param mid:
        :param dt_id:
        """
        model = self.load_one_model(mid)
        df = get_train_data(dt_id)
        self.train_model(model, df)
        return True
