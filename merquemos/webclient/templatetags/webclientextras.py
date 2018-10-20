from django import template
from stock.models import Product

register = template.Library()

@register.assignment_tag
def get_filtered_products(store, category):
    if category.parent is None:
        q =  Product.objects.filter(category__parent=category, store=store, is_active=True)
    else:
        q = Product.objects.filter(category=category, store=store, is_active=True)
    return q