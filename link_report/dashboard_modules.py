from admin_tools.dashboard.modules import DashboardModule
from django.utils.translation import ugettext_lazy as _


class Sentry404Errors(DashboardModule):
    title = _('Recent 404 Errors')
    template = 'admin_tools/dashboard/modules/sentry_404_errors.html'
    
    def __init__(self, title=None, **kwargs):
        kwargs.update({})
        super(Sentry404Errors, self).__init__(title, **kwargs)
    
    def init_with_context(self, context):
        if self._initialized:
            return
        
        self.pre_content = _('')
        self.post_content = _('')
        self._initialized = True
