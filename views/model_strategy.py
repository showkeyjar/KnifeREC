from adminlte.views import BaseAdminView


class ModelStrategyView(BaseAdminView):
    column_editable_list = ['name', 'type', 'pub_models', 'pub_percent', 'created_at']
    column_searchable_list = ['name', 'pub_models', 'created_at']
    column_exclude_list = None
    column_details_exclude_list = None
    column_filters = ['type', 'pub_models', 'created_at']
    can_export = True
    can_view_details = True
    can_create = True
    can_edit = True
    can_delete = True
    edit_modal = True
    create_modal = True
    details_modal = True
