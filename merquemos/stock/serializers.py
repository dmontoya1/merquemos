from django.contrib.sites.models import Site
from rest_framework import serializers
from .models import Store, Category, Product, Brand, BrandStore


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

class BrandSerializer(serializers.ModelSerializer):

    class Meta:
        model = Brand
        fields = ('pk', 'name')

class BrandStoreSerializer(serializers.ModelSerializer):

    class Meta:
        model = BrandStore
        fields = ('pk', 'brand', 'store')

class ProductSerializer(serializers.ModelSerializer):
    price = serializers.DecimalField(
        source='get_price',
        read_only=True,
        max_digits=10,
        decimal_places=2
    )
    discount_price = serializers.DecimalField(
        source='price',
        read_only=True,
        max_digits=10,
        decimal_places=2
    )
    product_image = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = (
            'pk',
            'sku',
            'name',
            'description',
            'price',
            'size',
            'product_image',
            'has_discount',
            'discount_price',
            'discount_percentage'
        )
    
    def get_product_image(self, obj):
        domain = Site.objects.get_current().domain
        return 'http://{domain}{path}'.format(domain=domain, path=obj.image.url)