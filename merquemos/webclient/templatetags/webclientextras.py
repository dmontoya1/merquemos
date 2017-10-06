from django import template
from stock.models import Product

register = template.Library()

@register.assignment_tag
def get_filtered_products(store, category):
    return Product.objects.filter(category__parent=category, store=store)