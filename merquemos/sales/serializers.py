from rest_framework import serializers
from .models import Order, Item


class OrderSerializer(serializers.ModelSerializer):
    item_quantity = serializers.IntegerField(source='get_item_quantity', read_only=True)
    total = serializers.DecimalField(
        source='get_total',
        read_only=True,
        max_digits=10,
        decimal_places=2
    )

    class Meta:
        model = Order
        fields = ('pk', 'item_quantity', 'total')

class ItemSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Item
        fields = ('product', 'order', 'quantity')