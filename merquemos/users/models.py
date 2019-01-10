# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import uuid

from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser

from allauth.socialaccount.models import SocialAccount

from manager.models import City

class User(AbstractUser):
    phone_number = models.CharField(
        max_length=15,
        blank=True,
        null=True
    )
    private_hash = models.UUIDField(
        editable=False
    )

    class Meta:
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"
    
    def __str__(self):
        if self.get_full_name() == "":
            return str(self.email)
        return str(self.get_full_name())
    
    def save(self, *args, **kwargs):
        if not self.private_hash:
            self.private_hash = uuid.uuid4()
        super(User, self).save(*args, **kwargs)

    def linked_social_account(self):
        if SocialAccount.objects.filter(user__pk=self.pk).count() > 0:
            return True
        return False

    def get_current_order(self):
        if self.related_orders.filter(status='PE').count() > 0:
            return self.related_orders.get(status='PE')
        elif self.related_orders.filter(status='AC').count() > 0:
            return self.related_orders.get(status='AC')
        elif self.related_orders.filter(status='SH').count() > 0:
            return self.related_orders.get(status='SH')
        return None


class Address(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="related_addresses")
    city = models.ForeignKey(City)
    name = models.CharField(max_length=25)
    phone_number = models.CharField(max_length=15)
    label = models.CharField(max_length=255)
    directions = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = "Dirección"
        verbose_name_plural = "Direcciones"
        ordering = ['-pk']

    def __str__(self):
        return "{} ({})".format(self.label, self.directions)

