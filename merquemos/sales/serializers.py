from rest_framework import serializers

from api.helpers import get_api_user
from stock.serializers import ProductSerializer
from users.serializers import AddressSerializer

from users.serializers import UserSerializer
from .models import Order, Item, Rating, DeliveryOrder


class OrderSerializer(serializers.ModelSerializer):
    item_quantity = serializers.IntegerField(source='get_item_quantity', read_only=True)

    store_id = serializers.ReadOnlyField(source='get_store_id')
    user = UserSerializer(many=False, read_only=True)

    class Meta:
        model = Order
        fields = ('pk', 'item_quantity', 'status', 'store_id', 'user')

class ItemSerializer(serializers.ModelSerializer):
    order = serializers.CharField(required=False)
    class Meta:
        model = Item
        fields = ('product', 'order', 'quantity')
    
    def create(self, validated_data):
        order = validated_data['order']
        for item in order.get_items():
            if item.product == validated_data['product']:
                item.quantity = item.quantity + validated_data['quantity']
                item.save()
                return item
        return Item.objects.create(**validated_data)

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
        fields = ('payment_method', 'status', 'address', 'extra_details', 'paid_amount', 'delivery_option', 'delivery_time')

class OrderDetailSerializer(OrderItemSerializer):
    delivery_order = DeliveryOrderSerializer(many=False, read_only=True)
    user = UserSerializer(many=False, read_only=True)

    class Meta:
        model = Order
        fields = ('pk', 'user', 'items', 'total_no_tax', 'total_tax', 'delivery_price', 'total_with_tax', 'delivery_order', 'status')

class OrderHistorySerializer(OrderItemSerializer):
    store_logo = serializers.SerializerMethodField()
    formated_last_status_date = serializers.DateTimeField(format="%Y-%m-%d", source="last_status_date", read_only=True)
    rating = serializers.IntegerField(source="get_rating", read_only=True)
    user = UserSerializer(many=False, read_only=True)

    class Meta:
        model = Order
        fields = ('pk', 'formated_last_status_date', 'status', 'store_logo', 'rating', 'total_with_tax', 'user')
    
    def get_store_logo(self, obj):
        if obj.related_items.all().count() > 0:
            if obj.related_items.all().last().product.store.logo:
                request = self.context.get('request')
                return request.build_absolute_uri(obj.related_items.all().last().product.store.logo.url)
        return None

class RatingSerializer(serializers.ModelSerializer):
    user = serializers.CharField(required=False)

    class Meta:
        model = Rating
        fields = ('user', 'order', 'number', 'comments')