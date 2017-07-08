# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.exceptions import ValidationError
from django.db import models

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

    def __unicode__(self):
        return 'App policy record'

    def clean(self):
        # Don't allow to save new AppPolicy objects is there is a created record.
        if self.__class__.objects.all().count() > 0:
            raise ValidationError('An AppPolicy record is already created')

class FAQCategory(models.Model):
    """Stores Frequently Asked Quetions categories
    """

    name = models.CharField(
        max_length=30,
        unique=True
    )

    def __unicode__(self):
        return self.name

class FAQItem(models.Model):
    """Stores FAQ questions per category (FAQCategory)
    """

    category = models.ForeignKey(FAQCategory)
    question = models.TextField(unique=True)
    answer = models.TextField(unique=True)

    def __unicode__(self):
        return self.question

class State(models.Model):
    """Stores country states
    """

    name = models.CharField(max_length=255)

    def __unicode__(self):
        return self.name

class City(models.Model):
    """Stores country cities, referenced by state (State). e.g: Pereira (City), Risaralda (State)
    """

    state = models.ForeignKey(State)
    name = models.CharField(max_length=255)

    def __unicode__(self):
        return self.name

