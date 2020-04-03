from . import db

"""
模型监控

id          编号
name        监控指标：ctr/cvr/acc/recall/psi/perplex 准确率/召回率/群体稳定性/困惑度
type        指标类型：user/data/sys 用户指标/数据指标/系统指标
group       发布组：model_pub id
created_at  创建时间
"""


class ModelMonitor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), default="")
    type = db.Column(db.String(100), default="")
    group = db.Column(db.String(255), default="")
    created_at = db.Column(db.DateTime(), nullable=False)
