from . import db

"""
模型训练

id          编号
name        模型实例名称
type        模型类型：排序/协同过滤/文本/深度网络
model       模型名称：sort/fm/lda/din
fields      选用特征
created_at  创建时间
"""


class ModelTrain(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), default="")
    type = db.Column(db.String(100), default="")
    model = db.Column(db.String(100), default="")
    fields = db.Column(db.String(255), default="")
    created_at = db.Column(db.DateTime(), nullable=False)
