from datetime import datetime
from django.db import transaction
from django.http import Http404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from general_util.constant import StatusTypeEnum
from general_util.permissions import IsOwnerOrReadOnly
from iha.models import IHA, IHAUsageCalendar
from iha.serializers import IHASerializer
from iha.util.util_functions import post_delete_iha

"""
Rest Framework API'leri için ayrı bi view dosyası oluşturulmuştur.
Burada işlevselliğine göre Rest Framework kullanarak API'ler yazılmış ve permissionları verilmiştir.

Not: Response dönüşlerinin aynı ve daha açıklayıcı(data,status,err_msg) bir katman eklenebilir.
"""


class IHADetail(APIView):
    """
    UUID'si belirli İHA'nın detaylarını görmek ve sahibinin o İHA'yı silebilmesi için yazılmış API.
    Kontrolü permission classes ile sağlanmaktadır.
    """
    permission_classes = [IsOwnerOrReadOnly]

    def get_object(self, uuid):
        try:
            return IHA.objects.get(uuid=uuid, activity_status=StatusTypeEnum.active.value)
        except IHA.DoesNotExist:
            raise Http404

    def get(self, request, uuid):
        iha_obj = self.get_object(uuid)
        serializer = IHASerializer(iha_obj)
        return Response(serializer.data)

    def delete(self, request, uuid):
        with transaction.atomic():  # Öncelikle kiralama istekleri daha sonrasında İHA pasife alındığı için olası bir hatada meydana gelecek veri tutarsızlığını engellemek adına transaction içine alınmıştır.
            post_delete_iha(uuid)
            iha_obj = self.get_object(uuid)
            iha_obj.activity_status = StatusTypeEnum.passive.value
            iha_obj.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class IHARequestRentalDate(APIView):
    """
    IHA kiralama talebi oluşturmak için kullanılan API
    """
    permission_classes = [IsAuthenticated]

    def get_object(self, uuid):
        try:
            return IHA.objects.get(uuid=uuid, activity_status=StatusTypeEnum.active.value)
        except IHA.DoesNotExist:
            raise Http404

    def post(self, request, uuid):
        response = {
            "status": False
        }
        datetime_format = '%Y-%m-%dT%H:%M'
        start_date = datetime.strptime(request.data['start_date'], datetime_format)
        end_date = datetime.strptime(request.data['end_date'], datetime_format)
        if IHAUsageCalendar.objects.check_date(uuid, start_date, end_date):
            iha_usage_calendar = IHAUsageCalendar()
            iha_usage_calendar.iha = self.get_object(uuid)
            iha_usage_calendar.start_date = start_date
            iha_usage_calendar.end_date = end_date
            iha_usage_calendar.renter = request.user
            iha_usage_calendar.save()
            response['status'] = True
        return Response(response)


class IHAUsageRequestByRenter(APIView):
    """
    IHA'yi kiralayan kişinin, kiralama bilgisini güncellemesi veya kiralamayı iptal etmesi için kullanılan API
    """
    permission_classes = [IsAuthenticated]

    def get_object(self, uuid, user):
        try:
            return IHAUsageCalendar.objects.get(uuid=uuid, activity_status=StatusTypeEnum.active.value, renter=user)
        except IHA.DoesNotExist:
            raise Http404

    def delete(self, request, uuid):
        iha_usage_obj = self.get_object(uuid, request.user)
        iha_usage_obj.cancelled_by_renter = True
        iha_usage_obj.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def patch(self, request, uuid):
        iha_usage_obj = self.get_object(uuid, request.user)
        response = {
            "status": False
        }
        datetime_format = '%Y-%m-%dT%H:%M'
        start_date = datetime.strptime(request.data['start_date'], datetime_format)
        end_date = datetime.strptime(request.data['end_date'], datetime_format)
        if IHAUsageCalendar.objects.check_date(iha_usage_obj.iha.uuid, start_date, end_date):
            iha_usage_obj.start_date = start_date
            iha_usage_obj.end_date = end_date
            iha_usage_obj.save()
            response['status'] = True
        return Response(response)


class IHAUsageRequestByOwner(APIView):
    """
    IHA sahibinin, IHA'yi kiralamak isteyenleri onayladığı ve reddettiği API
    """
    permission_classes = [IsAuthenticated]

    def get_object(self, uuid, user):
        try:
            return IHAUsageCalendar.objects.get(uuid=uuid, activity_status=StatusTypeEnum.active.value, iha__owner=user)
        except IHA.DoesNotExist:
            raise Http404

    def post(self, request, uuid):
        iha_usage_obj = self.get_object(uuid, request.user)
        response = {
            "status": False
        }
        payload_data = request.data.get('status', None)  # Burada serializer kullanılabilir bu şekilde ilerletmek yerine
        if payload_data is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        payload_data = True if payload_data == "true" else False
        if payload_data is True:  # TODO Burası YENİ!!!
            if IHAUsageCalendar.objects.check_date(iha_usage_obj.iha.uuid, iha_usage_obj.start_date,
                                                   iha_usage_obj.end_date):
                iha_usage_obj.approved_by_lessor = True
                response['status'] = True
        else:
            iha_usage_obj.cancelled_by_lessor = True
            response['status'] = True
        iha_usage_obj.save()
        return Response(response)
