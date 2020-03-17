from . import db

"""
模型监控

id          编号
tabname     表名称
type        表类型：用户/商品/商家
fields      特征名称
fields_type 特征类型：数值/分类
created_at  创建时间
"""


class ModelMonitor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tabname = db.Column(db.String(100), default="")
    type = db.Column(db.String(100), default="")
    fields = db.Column(db.String(255), default="")
    fields_type = db.Column(db.String(255), default="")
    created_at = db.Column(db.DateTime(), nullable=False)
