"""
URL configuration for ihaproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
                  path('auth/', include('authentication.urls')),
                  path('profile/', include('user.urls')),
                  path('iha/', include('iha.urls')),
                  path('admin/', admin.site.urls),
                  path('api/v1/iha/', include('iha.api_urls')),
                  # API'ler direkt farklı bir uzantı ile kullanılmıştır. Eğer ileride güncelleme yapılırsa sadece versiyon değiştirilip ekleme yapılabilir.
                  path('', include('core.urls')),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL,
                                                                                         document_root=settings.STATIC_ROOT)
