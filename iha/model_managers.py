from django.db import models
from django.db.models import Q

from general_util.constant import StatusTypeEnum

"""
Açıklama:
Model Manager oluşturmaktaki sebep sorguları tek bir yerden sağlamak ve view içlerinde sorgu yazılmasını en az seviyeye indirmektir.
Bu sayede aynı sorguları farklı farklı yerlerde tek bir çatı altında kullanabiliyoruz gerekirse güncelleyebiliyoruz.
"""


class IHAModelManager(models.Manager):
    # Burası IHA modeli için oluşturulmuş bir model managerdır. IHA için gerekli sorgular buraya yazılıp o şekilde servis edilecektir.
    def get_all_by_user(self, user):
        # Kullanıcıya ait İHA'ların DB'den çekildiği yer
        q1 = Q(owner=user)
        q2 = Q(activity_status=StatusTypeEnum.active.value)
        return super().get_queryset().filter(q1 & q2).order_by('-created_at')

    def get_by_uuid(self, uuid, user):
        # Kullanıcıya ait İHA'nın uuid'sine göre DB'den çekildiği yer
        q1 = Q(owner=user)
        q2 = Q(activity_status=StatusTypeEnum.active.value)
        q3 = Q(uuid=uuid)
        return super().get_queryset().filter(q1 & q2 & q3).first()

    def get_all(self):
        # Tüm İHA'ların DB'den çekildiği yer
        q1 = Q(activity_status=StatusTypeEnum.active.value)
        return super().get_queryset().filter(q1).order_by('-created_at')


class IHAUsageCalendarModelManager(models.Manager):
    # Burası IHAUsageCalendar modeli için oluşturulmuş bir model managerdır. IHAUsageCalendar için gerekli sorgular buraya yazılıp o şekilde servis edilecektir.

    def get_all_by_renter_user(self, user):
        # Bir Kullanıcı tüm ilanlar kısmından kiraladığı tüm İHA'ları listelemek için kullanılan sorgu
        q1 = Q(renter=user)
        q2 = Q(activity_status=StatusTypeEnum.active.value)
        return super().get_queryset().filter(q1 & q2).order_by('-created_at')

    def check_date(self, iha_uuid, request_start_date, request_end_date):
        # Bir Kullanıcı tüm ilanlar kısmından kiralamak istediği zaman girdiği tarih kontrol edilmesi gerekiyor o tarihte müsait mi diye. Bu kontrol için
        # yazılmış sorgudur. Eğer tarih müsaitse True dönecek yoksa False.
        q1 = Q(iha__uuid=iha_uuid)
        q2 = Q(iha__activity_status=StatusTypeEnum.active.value)
        q3 = Q(cancelled_by_renter=False)
        q4 = Q(cancelled_by_lessor=False)
        q5 = Q(approved_by_renter=True)
        q6 = Q(approved_by_lessor=True)
        q7 = Q(end_date__gte=request_start_date)
        q8 = Q(end_date__lte=request_end_date)
        q9 = Q(start_date__gte=request_start_date)
        q10 = Q(start_date__lte=request_end_date)
        q11 = Q(activity_status=StatusTypeEnum.active.value)
        return not super().get_queryset().filter(q1 & q2 & q3 & q4 & q5 & q6 & ((q7 & q8) | (q9 & q10)) & q11).exists()

    def check_unanswered(self, iha_uuid):
        # İHA için oluşturulmuş kiralama isteğinin cevaplanıp cevaplanmadığını kontrol eden sorgu
        q1 = Q(iha__uuid=iha_uuid)
        q2 = Q(iha__activity_status=StatusTypeEnum.active.value)
        q3 = Q(cancelled_by_renter=False)
        q4 = Q(cancelled_by_lessor=False)
        q5 = Q(approved_by_lessor=False)
        return super().get_queryset().filter(q1 & q2 & q3 & q4 & q5).exists()

    def get_unanswered(self, iha_uuid):
        # İHA için oluşturulmuş kiralama isteğinin cevaplanmayan kayıtları getiren sorgu
        q1 = Q(iha__uuid=iha_uuid)
        q2 = Q(iha__activity_status=StatusTypeEnum.active.value)
        q3 = Q(cancelled_by_renter=False)
        q4 = Q(cancelled_by_lessor=False)
        q5 = Q(approved_by_lessor=False)
        return super().get_queryset().filter(q1 & q2 & q3 & q4 & q5)

    def get_all_by_iha_uuid_and_owner(self, user, uuid):
        # Kullanıcı ve İHA UUID'sine göre tüm kayıtları getiren sorgu
        q1 = Q(iha__owner=user)
        q2 = Q(iha__activity_status=StatusTypeEnum.active.value)
        q3 = Q(iha__uuid=uuid)
        return super().get_queryset().filter(q1 & q2 & q3).order_by('-created_at')
