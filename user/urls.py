from django.urls import path

from user.views import profile

app_name = "user"

urlpatterns = [
    path('', profile, name="profile"),
]
