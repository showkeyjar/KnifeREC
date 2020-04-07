from flask import request
from ml.data.utils import *
from flask_admin import expose
from adminlte.views import BaseAdminView


class DataFeatureView(BaseAdminView):
    list_template = 'admin/model/data_feature_list.html'
    column_editable_list = ['name', 'dt_id', 'data_type', 'rule_type', 'rules', 'created_at']
    column_searchable_list = ['name', 'dt_id', 'rules', 'created_at']
    column_exclude_list = None
    column_details_exclude_list = None
    column_filters = ['dt_id', 'data_type', 'rule_type', 'created_at']
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
        df_id = request.args.get("id")
        df = preview_data_feature(df_id)
        # df = pd.DataFrame({'a':[1, 2], 'b':[3, 4], 'c':[5, 6]})
        return self.render('admin/model/preview.html',  tables=[df.to_html(classes='table table-bordered table-hover', header="true")])

