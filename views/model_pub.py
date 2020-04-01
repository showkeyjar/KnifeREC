from flask_admin import expose
from adminlte.views import BaseAdminView


class ModelPubView(BaseAdminView):
    list_template = 'admin/model/model_list.html'
    column_editable_list = ['model_id', 'type', 'period', 'start_at', 'created_at']
    column_searchable_list = ['model_id', 'type', 'start_at', 'created_at']
    column_exclude_list = None
    column_details_exclude_list = None
    column_filters = ['type', 'start_at', 'created_at']
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
        # todo 启动模型
        return self.render("admin/model/list.html", num_pages=1)

    @expose('/stop')
    def stop(self):
        # todo 停止模型
        return self.render("admin/model/list.html", num_pages=1)
