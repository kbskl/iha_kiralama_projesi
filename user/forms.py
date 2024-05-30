from django import forms
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User

from general_util.constant import GenderEnum


class UserForm(forms.ModelForm):
    username = forms.CharField(max_length=75,
                               widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
                               label="Email")
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'İsim'}),
                                 label="İsim")
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Soyisim'}),
                                label="Soyisim")
    gender = forms.ChoiceField(choices=GenderEnum.choices(), required=True, label="Cinsiyet")

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'gender']

    def save(self, commit=True, *args, **kwargs):
        gender = self.cleaned_data.pop('gender', None)
        user = super(UserForm, self).save(*args, **kwargs)
        user.profile.gender = gender
        user.profile.save()
        return user


class UserPasswordChangeForm(PasswordChangeForm):
    user = None
    old_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Eski Parola'}))
    new_password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Yeni Parola'}))
    new_password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Tekrar Yeni Parola'}))

    def save(self, commit=True):
        data = super(UserPasswordChangeForm, self).save(commit=False)
        data.email = data.username
        data.save()
        return data
