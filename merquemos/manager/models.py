# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.exceptions import ValidationError
from django.db import models
from django.utils.text import slugify

class AppPolicy(models.Model):
    """Stores application policies.
    """

    privacy_policy = models.TextField(
        null=True,
        blank=True
    )
    terms_and_conditions = models.TextField(
        null=True,
        blank=True
    )
    
    class Meta:
        verbose_name = 'Poliza de usuario'
        verbose_name_plural = 'Polizas de usuario'
        
    def __unicode__(self):
        return 'Registro de %s' % str(self._meta.verbose_name)

    def clean(self):
        # Don't allow to save new objects if there is a created record.
        if self.__class__.objects.all().count() > 0:
            raise ValidationError('An %s record is already created' % self._meta.verbose_name)
        return True

class FAQCategory(models.Model):
    """Stores Frequently Asked Quetions categories
    """

    name = models.CharField(
        max_length=30,
        unique=True
    )

    class Meta:
        verbose_name = 'Categoría de FAQ'
        verbose_name_plural = 'Categorías de FAQ'

    def __unicode__(self):
        return self.name

class FAQItem(models.Model):
    """Stores FAQ questions per category (FAQCategory)
    """

    category = models.ForeignKey(FAQCategory)
    question = models.TextField(unique=True)
    answer = models.TextField(unique=True)

    class Meta:
        verbose_name = 'Item de FAQ'
        verbose_name_plural = 'Items de FAQ'

    def __unicode__(self):
        return self.question

class State(models.Model):
    """Stores country states
    """

    name = models.CharField(max_length=255)

    class Meta:
        verbose_name = 'Region'
        verbose_name_plural = 'Regiones'

    def __unicode__(self):
        return self.name

class City(models.Model):
    """Stores country cities, referenced by state (State). e.g: Pereira (City), Risaralda (State)
    """

    state = models.ForeignKey(State, related_name="related_cities")
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, null=True, blank=True)

    class Meta:
        verbose_name = 'Ciudad'
        verbose_name_plural = 'Ciudades'

    def __unicode__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        name = self.state.name + "-" + self.name
        self.slug = slugify(name)
        super(City, self).save(*args, **kwargs)

class ContactMessage(models.Model):
    """Stores contact messages sent from contact form
    """

    title = models.CharField(max_length=255)
    content = models.TextField()

    class Meta:
        verbose_name = 'Mensaje de contacto'
        verbose_name_plural = 'Mensajes de contacto'

    def __unicode__(self):
        return self.title

