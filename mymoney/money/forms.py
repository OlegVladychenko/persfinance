from django import forms

from .models import *

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['id', 'sum','counterparty_id']
        widgets = {
            'id': forms.TextInput(attrs={'class': 'form-control'}),
            'sum': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'id': 'Заголовок',
            'sum': 'Сумма',
        }
