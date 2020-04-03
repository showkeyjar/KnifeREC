from . import db

"""
模型管理

id          编号
name        模型名称
type        模型类型：排序/协同过滤/文本/深度网络
code        模型代码：sort/fm/lda/din
file        模型文件：训练好的二进制文件
created_at  创建时间
"""


class ModelAdmin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), default="")
    type = db.Column(db.String(100), default="")
    code = db.Column(db.String(100), default="")
    file = db.Column(db.String(100), default="")
    created_at = db.Column(db.DateTime(), nullable=False)
