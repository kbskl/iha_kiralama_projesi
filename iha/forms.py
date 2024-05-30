from django import forms

from iha.models import IHA


class IHAForm(forms.ModelForm):
    class Meta:
        model = IHA
        fields = ['title', 'brand', 'model', 'communication_range', 'weight', 'length', 'category']
