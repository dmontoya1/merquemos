from rest_framework import serializers
from .models import Store, Category, Product


class StoreSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Store
        fields = (
            'pk',
            'name',
            'logo',
            'app_cover',
            'app_hex_code',
            'is_open'
        )

class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('pk', 'name')

class ProductSerializer(serializers.ModelSerializer):
    price = serializers.DecimalField(
        source='get_price',
        read_only=True,
        max_digits=10,
        decimal_places=2
    )

    class Meta:
        model = Product
        fields = (
            'pk',
            'code',
            'name',
            'description',
            'price',
            'size',
            'image',
            'has_discount',
            'discount_percentage'
        )