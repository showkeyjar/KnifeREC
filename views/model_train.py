from flask import request
from ml.model.utils import *
from flask_admin import expose
from adminlte.views import BaseAdminView


class ModelTrainView(BaseAdminView):
    list_template = 'admin/model/model_train_list.html'
    column_editable_list = ['name', 'type', 'model', 'fields', 'created_at']
    column_searchable_list = ['name', 'model', 'fields', 'created_at']
    column_exclude_list = None
    column_details_exclude_list = None
    column_filters = ['type', 'fields', 'created_at']
    can_export = True
    can_view_details = True
    can_create = True
    can_edit = True
    can_delete = True
    edit_modal = True
    create_modal = True
    details_modal = True

    @expose('/start')
    def start(self):
        #数据预览
        m_id = request.args.get("id")
        status = start_train_model(m_id)
        return status
