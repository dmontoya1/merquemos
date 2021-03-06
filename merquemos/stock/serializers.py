from django.contrib.sites.models import Site
from rest_framework import serializers
from .models import (
    Store, Category, Product,
    Brand, BrandStore, Inventory
)


class StoreSerializer(serializers.ModelSerializer):

    bank = serializers.SlugRelatedField(
        many=False,
        read_only=True,
        slug_field='name'
    )
    bank_type = serializers.SerializerMethodField()
    delivery_price = serializers.SerializerMethodField()

    def get_bank_type(self, obj):
        return obj.get_bank_type_display()

    def get_delivery_price(self, obj):
        return obj.related_parameters.get().delivery_price

    class Meta:
        model = Store
        fields = (
            'pk',
            'name',
            'logo',
            'app_cover',
            'app_hex_code',
            'is_open',
            'city',
            'address',
            'phone_number',
            'web_cover',
            'legal_id_number',
            'bank',
            'bank_type',
            'bank_number',
            'delivery_price'
        )


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('pk', 'name', 'parent')


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ('pk', 'name')


class BrandStoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = BrandStore
        fields = ('pk', 'brand', 'store')


class InventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Inventory
        fields = ('pk', 'product', 'quantity')


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
    product_price = serializers.DecimalField(
        source='price',
        max_digits=10,
        decimal_places=2
    )
    product_image = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = (
            'pk',
            'store',
            'brand',
            'category',
            'sku',
            'barcode',
            'name',
            'image',
            'description',
            'product_price',
            'price',
            'tax_percentage',
            'size',
            'product_image',
            'has_discount',
            'discount_price',
            'discount_percentage',
            'pum_type',
            'pum_value'
        )

    def get_product_image(self, obj):
        domain = Site.objects.get_current().domain
        return 'https://{domain}{path}'.format(domain=domain, path=obj.image.url)


class ProductDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = (
            'pk',
            'sku',
            'name',
            'image',
        )
        lookup_field = 'sku'
