from flask import request
from ml.data.utils import *
from flask_admin import expose
from adminlte.views import BaseAdminView


class DataTableView(BaseAdminView):
    list_template = 'admin/model/data_list.html'
    column_editable_list = ['tabname', 'type', 'fields', 'fields_type', 'created_at']
    column_searchable_list = ['tabname', 'fields', 'created_at']
    column_exclude_list = ['fields_type']
    column_details_exclude_list = None
    column_filters = ['type', 'fields_type', 'created_at']
    can_export = True
    can_view_details = True
    can_create = True
    can_edit = True
    can_delete = True
    edit_modal = True
    create_modal = True
    details_modal = True

    @expose('/preview')
    def preview(self):
        #数据预览
        dt_id = request.args.get("id")
        df = get_data(dt_id)
        # df = pd.DataFrame({'a':[1, 2], 'b':[3, 4], 'c':[5, 6]})
        return self.render('admin/model/preview.html',  tables=[df.to_html(classes='table table-bordered table-hover', header="true")])
