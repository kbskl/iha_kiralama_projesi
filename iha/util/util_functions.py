from iha.models import IHAUsageCalendar


def post_delete_iha(iha_uuid):
    """
    Açıklama:
    Bir İHA silindiği zaman buna ait açılmış kiralama isteklerininde iptal edilmesi gerekmektedir.
    Bunun için yazılmış bir fonksiyon
    """
    all_unanswered_requests = IHAUsageCalendar.objects.get_unanswered(iha_uuid)
    for request in all_unanswered_requests:
        request.cancelled_by_lessor = True
        request.save()
