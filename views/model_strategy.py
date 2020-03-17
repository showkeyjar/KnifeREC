from adminlte.views import BaseAdminView


class ModelStrategyView(BaseAdminView):
    column_editable_list = ['tabname', 'type', 'fields', 'fields_type', 'created_at']
    column_searchable_list = ['tabname', 'fields', 'created_at']
    column_exclude_list = None
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
