from . import db

"""
模型策略
包括：随机展示策略、均匀展示策略、强化学习策略、多轮对话策略

id          编号
name        组名
type        展示策略：random/average/reinforce/dialogue 随机/均匀/强化学习/多轮对话
pub_models  部署模型编号：1,2,3
pub_percent 部署模型占比：0.3,0.3,0.3
created_at  创建时间
"""


class ModelStrategy(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), default="")
    type = db.Column(db.String(100), default="")
    pub_models = db.Column(db.String(255), default="")
    pub_percent = db.Column(db.String(255), default="")
    created_at = db.Column(db.DateTime(), nullable=False)
