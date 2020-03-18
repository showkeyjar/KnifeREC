from . import db

"""
用户画像模型

id          源编号
names       源名称
type        连接方式：csv/odps/mysql
uri         连接地址
created_at  创建时间
"""


class PortraitUser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    names = db.Column(db.String(100), default="")
    type = db.Column(db.String(100), default="csv")
    uri = db.Column(db.String(255), default="")
    created_at = db.Column(db.DateTime(), nullable=False)
