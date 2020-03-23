from flask import Flask, url_for, render_template, jsonify, Config
from flask_migrate import Migrate
from flask_security import Security
from flask_security.utils import encrypt_password
from flask_admin import helpers as admin_helpers
from adminlte.admin import AdminLte, admins_store, admin_db
from adminlte.models import Role, User
from adminlte.views import FaLink, AdminsView

from flask_admin import menu

from models import db
from models.message import Message
from models.data_source import DataSource
from models.data_table import DataTable
from models.data_feature import DataFeature
from models.portrait_user import PortraitUser
from models.model_admin import ModelAdmin
from models.model_train import ModelTrain
from models.model_pub import ModelPub
from models.model_strategy import ModelStrategy
from models.model_monitor import ModelMonitor

from views.message import MessageView
from views.data_source import DataSourceView
from views.data_table import DataTableView
from views.data_feature import DataFeatureView
from views.portrait_user import PortraitUserView
from views.model_admin import ModelAdminView
from views.model_train import ModelTrainView
from views.model_pub import ModelPubView
from views.model_strategy import ModelStrategyView
from views.model_monitor import ModelMonitorView

from tools.utils import *

app = Flask(__name__)
# app.config.from_pyfile('config.ini')
# 需要后台调用，所以使用 configparser 读取
# 注意 working directory
conf_ini = read_flask_config()
app.config.from_mapping(conf_ini)


@app.route('/')
def index():
    sys_conf = {'title': 'KnifeREC', 'author': 'zergskj'}
    return render_template("index.html", sys=sys_conf)


@app.route('/predict')
def predict():
    result = {'user_id': '1', 'prod_id': ''}
    return jsonify(result)


db.init_app(app)
db.app = app
migrate = Migrate(app, db)
admin_migrate = Migrate(app, admin_db)

security = Security(app, admins_store)

admin = AdminLte(app, skin='green', name='KnifeREC', short_name="<b>K</b>R", long_name=u"<b>KnifeREC</b>推荐系统")


def create_menu():
    admin.add_view(DataSourceView(DataSource, db.session, name=u'数据源', menu_icon_value='fa-cube'))
    admin.add_view(DataTableView(DataTable, db.session, name=u"数据表", menu_icon_value='fa-table'))
    admin.add_view(DataFeatureView(DataFeature, db.session, name=u"特征工程", menu_icon_value='fa-filter'))

    admin.add_view(MessageView(Message, db.session, name=u"商家画像", menu_icon_value='fa-user-circle'))
    admin.add_view(PortraitUserView(PortraitUser, db.session, name=u"用户画像", menu_icon_value='fa-user'))

    admin.add_view(ModelAdminView(ModelAdmin, db.session, name=u"模型管理", menu_icon_value='fa-tasks'))
    admin.add_view(ModelTrainView(ModelTrain, db.session, name=u"模型训练", menu_icon_value='fa-tasks'))
    admin.add_view(ModelPubView(ModelPub, db.session, name=u"模型部署", menu_icon_value='fa-rocket'))

    admin.add_view(ModelStrategyView(ModelStrategy, db.session, name=u"策略设置", menu_icon_value='fa-gears'))
    admin.add_view(ModelMonitorView(ModelMonitor, db.session, name=u"模型监控", menu_icon_value='fa-laptop'))

    admin.add_view(AdminsView(User, admin_db.session, name="管理员", menu_icon_value='fa-user-secret'))
    admin.set_category_icon(name='Author', icon_value='fa-address-card')


@security.context_processor
def security_context_processor():
    return dict(
        admin_base_template=admin.base_template,
        admin_view=admin.index_view,
        h=admin_helpers,
        get_url=url_for
    )


@app.cli.command()
def build_sample_db():
    """
    Populate a small db with some example entries.
    """
    admin_db.drop_all()
    admin_db.create_all()

    with app.app_context():
        super_admin_role = Role(name='superadmin')
        admin_role = Role(name='admin')
        admin_db.session.add(super_admin_role)
        admin_db.session.add(admin_role)
        admin_db.session.commit()

        test_user = admins_store.create_user(
            first_name='John',
            last_name='Doe',
            email='admin@admin.com',
            password=encrypt_password('admin'),
            roles=[super_admin_role, admin_role]
        )
        admin_db.session.add(test_user)
        admin_db.session.commit()
    return


if __name__ == '__main__':
    create_menu()
    app.run()
