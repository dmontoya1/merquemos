from rest_framework import serializers
from .models import Store, Category, Product


class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = ('pk', 'name', 'logo', 'app_cover', 'app_hex_code')

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('pk', 'name')

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = (
            'pk',
            'code',
            'name',
            'description',
            'price',
            'size',
            'image'
        )