from import_export import resources
from import_export.fields import Field

from stock.models import Product
from sales.models import Order, DeliveryOrder, Rating


class ProductResource(resources.ModelResource):
    name = Field(attribute='name', column_name='nombre')
    price = Field(attribute='price', column_name='precio')
    count = Field(attribute='stock_quantity', column_name='cantidad')
    
    class Meta:
        model = Product
        fields = ('name', 'price', 'stock_quantity')
    

