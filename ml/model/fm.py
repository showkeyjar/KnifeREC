from lightfm import LightFM
from lightfm.datasets import fetch_movielens
from lightfm.evaluation import precision_at_k

"""
todo FM模型
"""


class FMModel:
    # Load the MovieLens 100k dataset. Only five
    # star ratings are treated as positive.
    def load_data(self):
        self.data = fetch_movielens(min_rating=5.0)

    def train_model(self):
        # Instantiate and train the model
        self.model = LightFM(loss='warp')
        self.model.fit(self.data['train'], epochs=30, num_threads=2)

    def test_model(self):
        # Evaluate the trained model
        test_precision = precision_at_k(self.model, self.data['test'], k=5).mean()

    def predict(self):
        # todo 预测结果
        return None
