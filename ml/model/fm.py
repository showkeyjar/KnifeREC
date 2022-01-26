from lightfm import LightFM
from lightfm.datasets import fetch_movielens
from lightfm.evaluation import precision_at_k

"""
todo FM模型
"""


class FMModel:
    def __init__(self):
        self.model_path = "data/model/fm.pkl"

    def load(self):
        self.model = LightFM(loss='warp')
        self.model.load(self.model_path)

    # Load the MovieLens 100k dataset. Only five
    # star ratings are treated as positive.
    def load_data(self):
        self.data = fetch_movielens(min_rating=5.0)

    def train(self, train_df):
        # Instantiate and train the model
        self.model = LightFM(loss='warp')
        self.model.fit(self.data['train'], epochs=30, num_threads=2)

    def test(self):
        # Evaluate the trained model
        test_precision = precision_at_k(self.model, self.data['test'], k=5).mean()

    def predict(self):
        # todo 预测结果
        return None


if __name__ == "__main__":
    fm = FMModel()
    fm.load_data()
    fm.train_model()
    result = fm.predict()
