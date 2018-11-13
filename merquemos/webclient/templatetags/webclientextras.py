from django import template
from stock.models import Product

register = template.Library()

@register.assignment_tag
def get_5_filtered_products(store, category):
    if category.parent is None:
        q =  Product.objects.filter(category__parent=category, store=store, is_active=True).order_by('name')[:6]
    else:
        q = Product.objects.filter(category=category, store=store, is_active=True).order_by('name')[:6]
    return q


@register.assignment_tag
def get_filtered_products(store, category):
    if category.parent is None:
        q =  Product.objects.filter(category__parent=category, store=store, is_active=True)
    else:
        q = Product.objects.filter(category=category, store=store, is_active=True)
    return q