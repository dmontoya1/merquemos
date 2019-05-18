from django import template
from users.models import User
from utils.models import ExportModelMixin


register = template.Library()

@register.filter(name="is_export_instance")
def is_export_instance(value):
    return isinstance(value, ExportModelMixin)

