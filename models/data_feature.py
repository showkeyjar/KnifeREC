from . import db

"""
特征工程

id          编号
dt_id       目标数据集
name        规则名称
data_type   数据类型：number/category/text/datetime/all
rule_type   规则类型：filter/replace/scale 筛选/替换/缩放
rules       规则：none>0.8 none:0   MinMaxScaler   LabelEncoder
created_at  创建时间
"""


class DataFeature(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    dt_id = db.Column(db.Integer)
    name = db.Column(db.String(100), default="")
    data_type = db.Column(db.String(100), default="")
    rule_type = db.Column(db.String(100), default="")
    rules = db.Column(db.String(255), default="")
    created_at = db.Column(db.DateTime(), nullable=False)
