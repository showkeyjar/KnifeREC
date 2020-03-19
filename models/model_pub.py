from . import db

"""
模型部署

id          编号
model_id    模型编号
type        部署类型：offline/online/feeds   离线/实时/feed流
period      模型生成周期：1-7day
start_at    运行时间：now/00:00:00
created_at  创建时间
"""


class ModelPub(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    model_id = db.Column(db.String(100), default="")
    type = db.Column(db.String(100), default="")
    period = db.Column(db.String(100), default="")
    start_at = db.Column(db.String(100), default="")
    created_at = db.Column(db.DateTime(), nullable=False)
