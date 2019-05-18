from importlib import import_module
try:
    from django.core.urlresolvers import reverse
except ImportError: # Django 1.11
    from django.urls import reverse

from django.template.loader import render_to_string
from jet.dashboard import modules
from jet.dashboard.dashboard import Dashboard, AppIndexDashboard
from jet.dashboard.models import UserDashboardModule
from django.utils.translation import ugettext_lazy as _
from jet.ordered_set import OrderedSet
from jet.utils import get_admin_site_name, context_to_dict

try:
    from django.template.context_processors import csrf
except ImportError:
    from django.core.context_processors import csrf

from reports.dashboard_modules import Reports

class IndexDashboard(Dashboard):
    columns = 3

    def init_with_context(self, context):
        self.available_children.append(modules.LinkList)
        self.available_children.append(modules.Feed)
        
        site_name = get_admin_site_name(context)
        # append a link list module for "quick links"
        self.children.append(modules.LinkList(
            _('Quick links'),
            layout='inline',
            draggable=False,
            deletable=False,
            collapsible=False,
            children=[
                [_('Return to site'), '/'],
                [_('Change password'),
                 reverse('%s:password_change' % site_name)],
                [_('Log out'), reverse('%s:logout' % site_name)],
            ],
            column=2,
            order=0
        ))


        # append an app list module for "Applications"
        self.children.append(modules.AppList(
            _('Applications'),
            exclude=('auth.*',),
            column=0,
            order=0
        ))
        self.children.append(Reports(
            'Reportes',
            column=1,
            order=0
        ))
