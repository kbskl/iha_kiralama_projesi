from django.urls import path

from iha.api_views import IHADetail, IHARequestRentalDate, IHAUsageRequestByRenter, IHAUsageRequestByOwner

"""
Rest Framework API'leri için ayrı bi url dosyası oluşturulmuştur.
"""
app_name = "api_iha"

urlpatterns = [
    path('detail/<str:uuid>/', IHADetail.as_view(), name="api-iha-detail"),
    path('request-rental/<str:uuid>/', IHARequestRentalDate.as_view(), name="api-iha-request-rental"),
    path('request-usage/renter/<str:uuid>/', IHAUsageRequestByRenter.as_view(), name="api-iha-request-usage-renter"),
    path('request-usage/owner/<str:uuid>/', IHAUsageRequestByOwner.as_view(), name="api-iha-request-usage-owner"),

]
