from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth.models import User
from django.db import transaction

from general_util.constant import GenderEnum


class LoginForm(forms.ModelForm):
    username = forms.CharField(max_length=75,
                               widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Parola'}))

    class Meta:
        model = User
        fields = ('username', 'password')

    def clean(self):
        if self.is_valid():
            username = self.cleaned_data['username']
            password = self.cleaned_data['password']
            if not authenticate(username=username, password=password):
                raise forms.ValidationError('Yanlış e-mail veya parola girildi. Lütfen kontrol edin.')


class RegisterForm(UserCreationForm):

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)

    username = forms.CharField(max_length=75,
                               widget=forms.EmailInput(attrs={'class': 'form-control'}),
                               label="Email")
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), label="Parola")
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}), label="Tekrar Parola")
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), label="İsim")
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', }), label="Soyisim")
    gender = forms.ChoiceField(choices=GenderEnum.choices(), required=True, label="Cinsiyet")

    class Meta:
        model = User
        fields = ["username", "password1", "password2", "first_name", "last_name", "gender"]

    def save(self, commit=True, *args, **kwargs):
        with transaction.atomic():
            gender = self.cleaned_data.pop('gender', None)
            user = super(RegisterForm, self).save(*args, **kwargs)
            user.profile.gender = gender
            user.profile.save()
        return user


