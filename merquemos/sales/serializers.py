from rest_framework import serializers

from stock.serializers import ProductSerializer
from .models import Order, Item


class OrderSerializer(serializers.ModelSerializer):
    item_quantity = serializers.IntegerField(source='get_item_quantity', read_only=True)

    class Meta:
        model = Order
        fields = ('pk', 'item_quantity')

class ItemSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Item
        fields = ('product', 'order', 'quantity')

class ItemDetailSerializer(serializers.ModelSerializer):
    product = ProductSerializer(many=False, read_only=True)

    class Meta:
        model = Item
        fields = ('pk', 'product', 'quantity', 'total')

class OrderItemSerializer(serializers.ModelSerializer):
    items = ItemDetailSerializer(many=True, read_only=True, source='get_items')
    total_tax = serializers.DecimalField(
        source='get_total_tax',
        read_only=True,
        max_digits=10,
        decimal_places=2
    )
    delivery_price = serializers.DecimalField(
        source='get_delivery_price',
        read_only=True,
        max_digits=10,
        decimal_places=2
    )
    total_no_tax = serializers.DecimalField(
        source='get_total_no_tax',
        read_only=True,
        max_digits=10,
        decimal_places=2
    )
    total_with_tax = serializers.DecimalField(
        source='get_total_with_tax',
        read_only=True,
        max_digits=10,
        decimal_places=2
    )

    class Meta:
        model = Order
        fields = ('pk', 'items', 'total_no_tax', 'total_tax', 'delivery_price', 'total_with_tax')