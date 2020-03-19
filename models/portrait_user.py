from . import db

"""
用户画像模型

id          标签编号
name        标签名称
type        标签类
user_id     用户编号
user_time   用户频次
created_at  创建时间
"""


class PortraitUser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), default="")
    type = db.Column(db.String(100), default="")
    user_id = db.Column(db.String(100), default="")
    user_time = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime(), nullable=False)
