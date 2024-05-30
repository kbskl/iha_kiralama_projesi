import uuid

from django.db import models
from django.utils import timezone

from general_util.constant import StatusTypeEnum

"""
Açıklama:
Uygulama içinde kullanılacak modellerde ortak olan değerler kategori haline getirilmiştir.
Kategori haline getirilen modeller abstract şekilde buradan servis edilmektedir.
"""


class GeneralModel(models.Model):
    updated_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(editable=False)
    deleted_at = models.DateTimeField(blank=True, null=True)
    activity_status = models.CharField(choices=StatusTypeEnum.choices(), max_length=50, verbose_name='Aktiflik Durumu',
                                       default=StatusTypeEnum.active.value)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.created_at:
            self.created_at = timezone.now()
        if self.activity_status == StatusTypeEnum.passive.value and self.deleted_at is None:
            self.deleted_at = timezone.now()
        self.updated_at = timezone.now()
        return super(GeneralModel, self).save(*args, **kwargs)


class UUIDModel(models.Model):
    uuid = models.CharField(max_length=255, unique=True, blank=True, null=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if self.uuid is None:
            self.uuid = uuid.uuid4()
        return super(UUIDModel, self).save(*args, **kwargs)
