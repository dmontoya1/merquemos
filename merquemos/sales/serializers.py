from rest_framework import serializers

from stock.serializers import ProductSerializer
from users.serializers import AddressSerializer

from .models import Order, Item, Rating, DeliveryOrder


class OrderSerializer(serializers.ModelSerializer):
    item_quantity = serializers.IntegerField(source='get_item_quantity', read_only=True)

    class Meta:
        model = Order
        fields = ('pk', 'item_quantity', 'status')

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

class DeliveryOrderSerializer(serializers.ModelSerializer):
    address = AddressSerializer(many=False, read_only=True)
    
    class Meta:
        model = DeliveryOrder
        fields = ('payment_method', 'status', 'address', 'extra_details', 'paid_amount')

class OrderDetailSerializer(OrderItemSerializer):
    deliveryorder = DeliveryOrderSerializer(many=False, read_only=True)

    class Meta:
        model = Order
        fields = ('pk', 'items', 'total_no_tax', 'total_tax', 'delivery_price', 'total_with_tax', 'deliveryorder', 'status')

class OrderHistorySerializer(OrderItemSerializer):
    store_logo = serializers.SerializerMethodField()
    formated_last_status_date = serializers.DateTimeField(format="%Y-%m-%d", source="last_status_date", read_only=True)

    class Meta:
        model = Order
        fields = ('pk', 'formated_last_status_date', 'status', 'store_logo', 'rating', 'total_with_tax')
    
    def get_store_logo(self, obj):
        if obj.related_items.all().last().product.store.logo:
            request = self.context.get('request')
            return request.build_absolute_uri(obj.related_items.all().last().product.store.logo.url)
        return None

class RatingSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.pk', required=False)

    class Meta:
        model = Rating
        fields = ('user', 'order', 'number', 'comments')