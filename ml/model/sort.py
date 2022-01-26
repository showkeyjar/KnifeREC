import dill
import pandas as pd

"""
排序模型
"""


class Sort:
    def __init__(self):
        self.data = "data/model/sort.pkl"
    
    def load(self):
        with open(self.data, 'rb') as in_strm:
            model = dill.load(in_strm)
        return model

    def sort(self, data, column, limit=20, asc=False):
        """
        todo 按指定字段排序
        """
        try:
            data.sort_values(column, ascending=asc, inplace=True)
            ret_df = data[:limit]
        except:
            ret_df = None
        return ret_df

    def train(self, train_df, label):
        """
        训练模型（将排序结果序列化到pkl）
        """
        sort_df = self.sort(train_df, label)
        with open(self.data, 'wb') as out_strm:
            dill.dump(sort_df, out_strm)

    def predict(self, features):
        with open(self.data, 'rb') as in_strm:
            sort_df = dill.load(in_strm)
        return sort_df[features]
