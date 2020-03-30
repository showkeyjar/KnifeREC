from . import db

"""
模型输出(输出结果管理)

id          编号
pub_id      模型部署编号
type        输出方式：csv/redis/mongo
uri         输出地址
created_at  创建时间
"""


class ModelOutput(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pub_id = db.Column(db.String(100), default="")
    type = db.Column(db.String(100), default="")
    uri = db.Column(db.String(255), default="")
    created_at = db.Column(db.DateTime(), nullable=False)
