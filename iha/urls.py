from django.urls import path

from iha.views import my_iha_list, add_iha, update_iha, get_all_iha, get_my_rented, my_iha_rental_detail

app_name = "iha"

urlpatterns = [
    # İHA'larım End Pointleri
    path('my-profile', my_iha_list, name="my-iha"),
    path('my-profile/add', add_iha, name="add-iha"),
    path('my-profile/update/<str:uuid>/', update_iha, name="update-iha"),
    path('my-profile/rental-detail/list/<str:uuid>/', my_iha_rental_detail, name="my-iha-rental-detail"),

    # Tüm ilanlar End Pointleri
    path('all-iha', get_all_iha, name="all-iha"),

    # Kiraladığım İHA'larım End Pointleri
    path('my-rented', get_my_rented, name="my-rented"),
]
