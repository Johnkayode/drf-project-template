import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _

from .managers import BaseManager, SoftDeleteManager


class BaseModel(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    deleted_at = models.DateTimeField(_("deleted"), null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True, db_index=True)

    objects = BaseManager()

    class Meta:
        abstract = True
