from flask_admin import expose, AdminIndexView


class IndexView(AdminIndexView):

    @expose('/')
    def default(self):
        dt = {
                'gmv': '100',
                'ctr': '53',
                'cvr': '8'
            }
        return self.render('admin/index.html', dt=dt)
