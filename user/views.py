from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from user.forms import UserForm, UserPasswordChangeForm

"""
Açıklama:
Kullanıcının kendi için yaptığı işlemler bu app altında toplanmıştır.
Kullanıcı burada kendi profilini güncelleyebilir veya şifresini değiştirebilir.
"""


@login_required
def profile(request):
    user_form = UserForm(instance=request.user, initial={'gender': request.user.profile.gender})
    password_form = UserPasswordChangeForm(user=request.user)
    if request.POST and 'updateUserManagerProfile' in request.POST:
        user_form = UserForm(request.POST, instance=request.user)
        if user_form.is_valid():
            user_form.save()
            messages.success(request, "Profil başarıyla güncellendi.")
            return redirect('user:profile')
    if request.POST and 'updatePassword' in request.POST:
        password_form = UserPasswordChangeForm(data=request.POST, user=request.user)
        if password_form.is_valid():
            password_form.save()
            update_session_auth_hash(request, request.user)
            messages.success(request, "Parola başarıyla güncellendi.")
            return redirect('user:profile')
    context = {
        "user_form": user_form,
        "password_form": password_form
    }
    return render(request, "user/profile.html", context)
