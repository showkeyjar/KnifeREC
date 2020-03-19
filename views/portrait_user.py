from adminlte.views import BaseAdminView


class PortraitUserView(BaseAdminView):
    column_editable_list = ['name', 'type', 'user_id', 'user_time', 'created_at']
    column_searchable_list = ['name', 'user_id', 'created_at']
    column_exclude_list = None
    column_details_exclude_list = None
    column_filters = ['type', 'created_at']
    can_export = True
    can_view_details = True
    can_create = True
    can_edit = True
    can_delete = True
    edit_modal = True
    create_modal = True
    details_modal = True
