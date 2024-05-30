import django_filters
from django.contrib.auth.models import User

from iha.models import IHA, IHAUsageCalendar

"""
Açıklama:
Django içinde kullanılacak filtrelemeler için bu dosya oluşturulmuştur.
Burada her bir view için özelleştirilmiş filtereleme yapıları bulunmaktadır.
Filtrelemelerin istekleri burada alan alan özelleştirilebilir.
"""


class IHAFilter(django_filters.FilterSet):
    created_at = django_filters.DateRangeFilter(label='Oluşturulma Aralığı')
    brand = django_filters.CharFilter(lookup_expr='icontains', label='Marka')
    model = django_filters.CharFilter(lookup_expr='icontains', label='Model')
    category = django_filters.CharFilter(lookup_expr='icontains', label='Kategori')
    weight = django_filters.NumberFilter(label="Maksimum Ağırlık (kg)",
                                         method="filter_weight")

    class Meta:
        model = IHA
        fields = ['created_at', 'brand', 'model', 'category', 'weight']

    def filter_weight(self, queryset, name, value):
        return queryset.filter(weight__lte=value)


class AllIHAFilter(django_filters.FilterSet):
    created_at = django_filters.DateRangeFilter(label='Oluşturulma Aralığı')
    brand = django_filters.CharFilter(lookup_expr='icontains', label='Marka')
    model = django_filters.CharFilter(lookup_expr='icontains', label='Model')
    category = django_filters.CharFilter(lookup_expr='icontains', label='Kategori')
    weight = django_filters.NumberFilter(label="Maksimum Ağırlık (kg)",
                                         method="filter_weight")
    owner = django_filters.ModelChoiceFilter(label="Sahibi",
                                             queryset=User.objects.filter(is_superuser=False).order_by(
                                                 "username"))

    class Meta:
        model = IHA
        fields = ['created_at', 'brand', 'model', 'category', 'weight']

    def filter_weight(self, queryset, name,
                      value):  # Ağırlık aslında geniş bir aralık olduğu için filtrelemede direkt o değeri arayacaktı. Bu yüzden bir fonksiyon yazıldı ve belirli bir değerden küçükler filtrelendi.
        return queryset.filter(weight__lte=value)


class IHAUsageCalendarFilter(django_filters.FilterSet):
    def __init__(self, *args, **kwargs):
        iha_qs = kwargs.pop('iha_qs', None)
        super(IHAUsageCalendarFilter, self).__init__(*args, **kwargs)
        if iha_qs is not None:
            self.filters["iha"] = django_filters.ModelChoiceFilter(queryset=iha_qs, label="İHA")

    created_at = django_filters.DateRangeFilter(label='Talebin Oluşturulma Aralığı')

    class Meta:
        model = IHAUsageCalendar
        fields = ['created_at', 'iha', 'cancelled_by_renter', 'cancelled_by_lessor',
                  'approved_by_lessor']


class IHARentalDetailsFilter(django_filters.FilterSet):
    def __init__(self, *args, **kwargs):
        renter_qs = kwargs.pop('renter_qs', None)
        super(IHARentalDetailsFilter, self).__init__(*args, **kwargs)
        if renter_qs is not None:
            self.filters["renter"] = django_filters.ModelChoiceFilter(queryset=renter_qs, label="Kiralayan")

    created_at = django_filters.DateRangeFilter(label='Talebin Oluşturulma Aralığı')

    class Meta:
        model = IHAUsageCalendar
        fields = ['created_at', 'renter', 'cancelled_by_renter', 'cancelled_by_lessor',
                  'approved_by_lessor']
