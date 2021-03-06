# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse_lazy
from django.utils.text import slugify

from manager.models import City, Bank


class Store(models.Model):

    AHORROS = 'AH'
    CORRIENTE = 'CO'

    BANK_TYPE = (
        (AHORROS, 'Ahorros'),
        (CORRIENTE, 'Corriente'),
    )

    name = models.CharField('Nombre', max_length=255, unique=True)
    legal_id_number = models.CharField('NIT', max_length=255, unique=True)
    manager = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name='Administrador',
        related_name='related_store',
        blank=True, null=True
    )
    logo = models.ImageField('logo', upload_to="stock/stores/logos/")
    city = models.ForeignKey(City, verbose_name='Ciudad', related_name="related_stores")
    address = models.CharField('Dirección', max_length=255)
    phone_number = models.CharField('Número telefónico', max_length=255)
    app_cover = models.ImageField(
        verbose_name='Imágen para Móvil',
        upload_to="stock/stores/app_covers/",
        null=True,
        blank=True
    )
    web_cover = models.ImageField(
        verbose_name='Imágen para Web',
        upload_to="stock/stores/web_covers/",
        null=True,
        blank=True
    )
    app_hex_code = models.CharField('Código HEX color', max_length=10, null=True, blank=True)
    slug = models.SlugField(unique=True, null=True, blank=True)
    is_active = models.BooleanField('Tienda activa?', default=True)
    bank = models.ForeignKey(
        Bank,
        verbose_name='Banco',
        null=True, blank=True
    )
    bank_type = models.CharField(
        'Tipo de cuenta',
        choices=BANK_TYPE,
        max_length=2,
        null=True,
        blank=True
    )
    bank_number = models.CharField(
        'Numero de cuenta',
        max_length=20,
        null=True, blank=True
    )

    class Meta:
        verbose_name = "Tienda"

    def __str__(self):
        return str(self.name)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Store, self).save(*args, **kwargs)

    def get_delivery_price(self):
        if self.related_parameters.all().count() > 0:
            params = self.related_parameters.all().last()
            return params.delivery_price
        return 0

    @models.permalink
    def get_absolute_url(self):
        return reverse_lazy('webclient:store', args=(self.city.name, self.slug))

    def is_open(self):
        if self.related_hours.all().count() > 0:
            return True
        return True

    def get_web_cover_url(self):
        if self.web_cover:
            return self.web_cover.url
        else:
            return ''


class StoreContact(models.Model):
    store = models.ForeignKey(Store, related_name='related_contacts')
    name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField()
    occupation = models.CharField(max_length=255)

    class Meta:
        verbose_name = "Contacto"

    def __str__(self):
        return str(self.name)


class StoreHour(models.Model):
    DAY_CHOICES = (
        (1, 'Lunes'),
        (2, 'Martes'),
        (3, 'Miercoles'),
        (4, 'Jueves'),
        (5, 'Viernes'),
        (6, 'Sábado'),
        (7, 'Domingo'),
    )
    store = models.ForeignKey(Store, related_name='related_hours')
    day = models.CharField(max_length=1, choices=DAY_CHOICES)
    open_time = models.TimeField()
    close_time = models.TimeField()

    class Meta:
        verbose_name = "Horario"
        unique_together = ('store', 'day')

    def __str__(self):
        return str(self.day.get_display_name())


class StoreParameter(models.Model):
    store = models.ForeignKey(Store, related_name='related_parameters')
    delivery_price = models.DecimalField('Precio Domicilio', max_digits=10, decimal_places=2, default=0)

    def __unicode__(self):
        return "Parámetro de la tienda"

    class Meta:
        verbose_name = "Parámetro de tienda"
        verbose_name_plural = "Parámetros de tiendas"


class Brand(models.Model):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        verbose_name = "Marca"

    def __str__(self):
        return str(self.name)


class BrandStore(models.Model):
    brand = models.ForeignKey(Brand)
    store = models.ForeignKey(Store)

    class Meta:
        verbose_name = "Marca por tienda"
        verbose_name_plural = "Marcas por tiendas"

    def __str__(self):
        return str(self.brand)


class Category(models.Model):
    name = models.CharField(max_length=255)
    parent = models.ForeignKey('self', null=True, blank=True, related_name="related_categories")
    slug = models.SlugField(unique=True, null=True, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Categoría"
        ordering = ['name', ]

    def __str__(self):
        return str(self.name)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    def get_related_products(self, store=None):
        if self.parent is not None:
            queryset = self.related_products.all()
        else:
            queryset = Product.objects.filter(category__parent=self)
        if store is not None:
            queryset = queryset.filter(store=store)
        return queryset


class Product(models.Model):
    GRAMO = 'GR'
    KILOGRAMO = 'KG'
    MILILITRO = 'ML'
    LITRO = 'LT'
    CENTIMETRO = 'CM'
    METRO = 'MT'

    PUM = (
        (GRAMO, 'Gramo'),
        (KILOGRAMO, 'Kilogramo'),
        (MILILITRO, 'Mililitro'),
        (LITRO, 'Litro'),
        (CENTIMETRO, 'Centimetro'),
        (METRO, 'Metro')
    )

    store = models.ForeignKey(Store)
    brand = models.ForeignKey(BrandStore)
    category = models.ForeignKey(Category, related_name='related_products')
    sku = models.CharField(max_length=255)
    barcode = models.TextField(null=True, blank=True)
    name = models.CharField(max_length=255, unique=True, )
    description = models.TextField()
    image = models.ImageField(upload_to="stock/products/images/", default="logo.png")
    tax_percentage = models.DecimalField(max_digits=10, decimal_places=2)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    size = models.CharField(max_length=255)
    stock_quantity = models.PositiveIntegerField(editable=False, default=0)
    discount_percentage = models.PositiveIntegerField(default=0)
    slug = models.SlugField(unique=True, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    date_added = models.DateField(auto_now_add=True)
    pum_value = models.DecimalField(
        'Precio por unidad de medida',
        decimal_places=2,
        max_digits=10,
        default=0
    )
    pum_type = models.CharField(
        'Unidad de medida',
        max_length=2,
        choices=PUM,
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = "Producto"
        ordering = ['name', ]

    def __str__(self):
        return str(self.name)

    def clean(self):
        if self.category.parent is None:
            raise ValidationError("La categoría seleccionada para el producto no puede ser {}, pues es una categoría principal. Por favor,\
            selecciona una subcategoría".format(self.category.name))

    def save(self, *args, **kwargs):
        name = self.name.replace('.', '')
        self.slug = slugify(name)
        super(Product, self).save(*args, **kwargs)

    def has_discount(self):
        if self.discount_percentage > 0:
            return True
        return False

    def get_discount_value(self):
        return self.discount_percentage * self.price / 100

    def get_tax_value(self):
        return self.tax_percentage * self.price / 100

    def get_price(self):
        if self.has_discount():
            return self.price - self.get_discount_value()
        return self.price

    def get_price_no_tax(self):
        return self.get_price() - self.get_tax_value()

    def get_image_url(self):
        if self.image:
            return self.image.url
        return None


class Inventory(models.Model):
    product = models.ForeignKey(Product)
    quantity = models.PositiveIntegerField()
    date_added = models.DateTimeField(auto_now_add=True, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True)

    class Meta:
        verbose_name = "Inventario"

    def __str__(self):
        return str(self.quantity)

    def __init__(self, *args, **kwargs):
        super(Inventory, self).__init__(*args, **kwargs)
        # Save last quantity value
        self.last_quantity = self.quantity

    def save(self, raw=False, *args, **kwargs):
        if raw is False:
            # Increase product stock quantity when Inventory object is saved
            self.last_quantity
            self.product.stock_quantity = self.product.stock_quantity + self.quantity
            self.product.save()
            super(Inventory, self).save(*args, **kwargs)

