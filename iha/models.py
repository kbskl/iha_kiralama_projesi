from django.contrib.auth.models import User
from django.db import models

from general_util.model import GeneralModel, UUIDModel
from iha.model_managers import IHAModelManager, IHAUsageCalendarModelManager


class IHA(GeneralModel, UUIDModel):
    title = models.CharField(verbose_name='Başlık', blank=True, null=True,
                             max_length=255)
    brand = models.CharField(verbose_name='Marka', max_length=255)
    model = models.CharField(verbose_name='Model', max_length=255)
    communication_range = models.CharField(verbose_name='Haberleşme Menzili', max_length=50, blank=True, null=True)
    weight = models.DecimalField(verbose_name='Ağırlık (kg)', decimal_places=2, max_digits=10, blank=True, null=True)
    length = models.DecimalField(verbose_name='Uzunluk (mt)', decimal_places=2, max_digits=10, blank=True, null=True)
    category = models.CharField(verbose_name='Kategori', max_length=50, blank=True, null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Sahibi")
    objects = IHAModelManager()

    def __str__(self):
        return f"{self.brand} - {self.model}"

    def save(self, *args, **kwargs):
        # DB tarafında tüm kolonların aynı olması için bu aşamada belirli methodlar uygulanmıştır.
        self.brand = self.brand.title()
        self.model = self.model.title()
        if self.title:
            self.title = self.title.title()
        if self.communication_range:
            self.communication_range = self.communication_range.upper()
        if self.category:
            self.category = self.category.title()
        return super(IHA, self).save(*args, **kwargs)

    def check_unanswered_request(self):
        # Django template kısmında gösterebilmemiz için yazılmış ve mevcut İHA'nın cevaplandırılmamış kiralama isteği olup olmadığını gösteren fonksiyon
        return IHAUsageCalendar.objects.check_unanswered(self.uuid)

    class Meta:
        indexes = [
            models.Index(fields=['owner', 'activity_status']),
            # Model manager'da yazılan sorgulara göre indexler oluşturulmuştur
            models.Index(fields=['uuid', 'owner', 'activity_status']),
        ]


class IHAUsageCalendar(GeneralModel, UUIDModel):
    iha = models.ForeignKey(IHA, on_delete=models.CASCADE, verbose_name="IHA")
    start_date = models.DateTimeField(verbose_name="Kiralama Başlama Tarihi")
    end_date = models.DateTimeField(verbose_name="Kiralama Bitiş Tarihi")
    renter = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Kiralayan")
    cancelled_by_renter = models.BooleanField(default=False, verbose_name="Kiralayan Kişi Tarafından İptal Edildi")
    cancelled_by_lessor = models.BooleanField(default=False, verbose_name="Kiraya Veren Kişi Tarafından İptal Edildi")
    approved_by_renter = models.BooleanField(default=True, verbose_name="Kiralayan Kişi Tarafından Onaylandı")
    approved_by_lessor = models.BooleanField(default=False, verbose_name="Kiraya Veren Kişi Tarafından Onaylandı")
    objects = IHAUsageCalendarModelManager()

    class Meta:
        indexes = [
            models.Index(fields=['renter', 'activity_status']),
            # Model Manager içinde atılan sorguların ortak kümesine göre indexler oluşturulmuştur.
            models.Index(fields=['iha', 'activity_status'])
        ]
