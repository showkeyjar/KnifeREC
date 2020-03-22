from adminlte.views import BaseAdminView


class ModelMonitorView(BaseAdminView):
    column_editable_list = ['name', 'type', 'group', 'created_at']
    column_searchable_list = ['name', 'group', 'created_at']
    column_exclude_list = None
    column_details_exclude_list = None
    column_filters = ['type', 'group', 'created_at']
    can_export = True
    can_view_details = True
    can_create = True
    can_edit = True
    can_delete = True
    edit_modal = True
    create_modal = True
    details_modal = True
