from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseNotFound
from django.shortcuts import render, redirect
from iha.filters import IHAFilter, AllIHAFilter, IHAUsageCalendarFilter, IHARentalDetailsFilter
from iha.forms import IHAForm
from iha.models import IHA, IHAUsageCalendar


@login_required
def my_iha_list(request):
    my_iha_list = IHA.objects.get_all_by_user(
        request.user)  # Direkt model manager içinde yazılan fonksiyon çağırılıyor bu sayede view içinde sorgu yazılmamış oluyor.
    all_iha = IHAFilter(request.GET, queryset=my_iha_list)
    context = {
        "all_iha": all_iha,
        "new_iha_form": IHAForm()
    }
    return render(request, "iha/my_iha_list.html", context)


@login_required
def add_iha(request):
    if request.POST and 'newIhaSubmit' in request.POST:
        new_iha_form = IHAForm(request.POST)
        if new_iha_form.is_valid():
            new_iha = new_iha_form.save(commit=False)
            new_iha.owner = request.user
            new_iha.save()
            messages.success(request,
                             "Yeni İHA başarıyla eklendi.")  # Kullanıcıyı bilgilendirmek için messages kütüphanesi kullanılmıştır.
        else:
            messages.error(request, "Yeni İHA eklerken sorun oldu. Lütfen alanları kontrol edip tekrar deneyiniz.")
    return redirect('iha:my-iha')


@login_required
def update_iha(request, uuid):
    iha = IHA.objects.get_by_uuid(uuid, request.user)
    if iha is None:
        return HttpResponseNotFound()
    iha_form = IHAForm(instance=iha)
    if request.POST and 'ihaUpdate' in request.POST:
        iha_form = IHAForm(request.POST, instance=iha)
        if iha_form.is_valid():
            iha_form.save()
            messages.success(request, "İHA başarıyla güncellendi.")
            return redirect('iha:my-iha')
        else:
            messages.error(request, "İHA güncellerken sorun oldu. Lütfen alanları kontrol edip tekrar deneyiniz.")
    context = {
        "iha": iha,
        "iha_form": iha_form
    }
    return render(request, "iha/update_my_iha.html", context)


@login_required
def my_iha_rental_detail(request, uuid):
    iha = IHA.objects.get_by_uuid(uuid, request.user)
    if iha is None:
        return HttpResponseNotFound()
    request_get_data = request.GET.copy()
    request_get_data.setdefault('cancelled_by_renter',
                                False)  # Burada default olarak kullanıcı ilk sayfayı açtığında tüm kiralama geçmişi değil istekler görülmesi amaçlanmıştır.
    request_get_data.setdefault('cancelled_by_lessor', False)
    request_get_data.setdefault('approved_by_lessor', False)
    rental_detail_qs = IHAUsageCalendar.objects.get_all_by_iha_uuid_and_owner(request.user, uuid)
    renter_qs = User.objects.filter(pk__in=rental_detail_qs.values_list('renter', flat=True)) # Burada kullanıcı filtreleme alanında tüm user'ları görmesin sadece onunla ilgili olanları görmesi amaçlanmıştır.
    rental_details = IHARentalDetailsFilter(request_get_data, queryset=rental_detail_qs, renter_qs=renter_qs)
    context = {
        "rental_details": rental_details,
        "iha": iha
    }
    return render(request, "iha/my_iha_rental_details.html", context)


@login_required
def get_all_iha(request):
    all_iha_list = IHA.objects.get_all()
    all_iha = AllIHAFilter(request.GET, queryset=all_iha_list)
    context = {
        "all_iha": all_iha
    }
    return render(request, "iha/all_iha_list.html", context)


@login_required
def get_my_rented(request):
    all_iha_usage_qs = IHAUsageCalendar.objects.get_all_by_renter_user(request.user)
    iha_qs = IHA.objects.filter(pk__in=all_iha_usage_qs.values_list('iha', flat=True)) # Burada kullanıcı filtreleme alanında tüm İHA'ları görmesin sadece onunla ilgili olanları görmesi amaçlanmıştır.
    all_iha_usage = IHAUsageCalendarFilter(request.GET, queryset=all_iha_usage_qs, iha_qs=iha_qs)
    context = {
        "all_iha_usage": all_iha_usage
    }
    return render(request, "iha/my_rentals_list.html", context)
