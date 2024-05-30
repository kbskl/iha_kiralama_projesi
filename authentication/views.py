from django.contrib import auth, messages
from django.contrib.auth import authenticate
from django.shortcuts import render, redirect

from authentication.forms import LoginForm, RegisterForm

"""
Açıklama:
authentication app içinde giriş yapma,çıkış yapma, kayıt olma işlemleri yapılmaktadır. Bu işlemler için app oluşturulmuştur.
"""


def login(request):
    # Kullanıcının giriş yapması için kullandığımız fonksiyon.
    if request.user.is_authenticated:
        if 'next' in request.GET:
            return redirect(request.GET.get('next'))
        return redirect('core:dashboard')
    if request.POST:
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user:
                auth.login(request, user)
                if 'next' in request.POST:  # Eğer kullanıcı giriş yapmadan bir sayfaya erişmeye çalışırsa, giriş yaptıktan sonra onu istediği sayfaya göndermek için yazılmıştır.
                    return redirect(request.POST.get('next'))
                return redirect('core:dashboard')
    else:
        login_form = LoginForm()
    context = {
        'login_form': login_form,
    }
    return render(request, 'auth/login.html', context)


def register(request):
    if request.POST and 'registerSubmit' in request.POST:
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            register_form.save()
            messages.success(request,
                             "Kayıt işlemi başarılı. Lütfen giriş yapınız.")  # Django html tarafında kullanıcıyı bilgilendirmek için messages kütüphanesi kullanılmıştır.
            return redirect('authentication:login')
    else:
        register_form = RegisterForm()
    context = {
        'register_form': register_form,
    }
    return render(request, 'auth/register.html', context)


def logout(request):
    auth.logout(request)
    return redirect('authentication:login')
