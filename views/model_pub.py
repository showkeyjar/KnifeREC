from adminlte.views import BaseAdminView


class ModelPubView(BaseAdminView):
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
