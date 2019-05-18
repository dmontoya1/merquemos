from django.db import models
from django.utils import timezone
from django.utils.text import slugify


class ExportModelMixin(models.Model):
    """
    """

    deleted_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        abstract = True

