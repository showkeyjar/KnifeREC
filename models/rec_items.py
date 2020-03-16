from . import db

"""
推荐商品源

id          源编号
names       源名称
type        连接方式：csv/odps/mysql
uri         连接地址
fields      特征名称
fields_type 特征类型：数值/分类
created_at  创建时间
"""


class RecItems(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    names = db.Column(db.String(100), default="")
    type = db.Column(db.String(100), default="csv")
    uri = db.Column(db.String(255), default="")
    fields = db.Column(db.String(255), default="")
    fields_type = db.Column(db.String(255), default="")
    created_at = db.Column(db.DateTime(), nullable=False)
