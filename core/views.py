from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from iha.models import IHA, IHAUsageCalendar

"""
Açıklama:
core app'i uygulama içinde genel olarak kullanılacak işlemler için açılmıştır.
Dashboardda bunlardan biri olduğu için buraya eklenmiştir.
"""


@login_required
def dashboard(request):
    context = {
        "total_iha_count": IHA.objects.get_all().count(),
        "total_rented_count": IHAUsageCalendar.objects.get_all_by_renter_user(request.user).count(),
        "total_my_iha_count": IHA.objects.get_all_by_user(request.user).count()
    }
    return render(request, "core/dashboard.html", context)
