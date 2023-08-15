from django import forms

from .models import *


class DateInput(forms.DateInput):
    input_type = 'date'


class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['id', 'sum', 'counterparty']
        widgets = {
            'id': forms.TextInput(attrs={'class': 'form-control'}),
            'sum': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'id': 'Заголовок',
            'sum': 'Сумма',
        }


class AddDebitDocForm(forms.Form):
    date = forms.DateField(widget=DateInput)
    type = forms.IntegerField()
    sum = forms.DecimalField()



    counterparty = forms.ModelChoiceField(
        label="Контрагент",
        queryset=Сounterparty.objects.all(),
        required=False,
        widget=forms.Select
    )

    category = forms.ModelChoiceField(
        label="Категория",
        queryset=Category.objects.all(),
        required=False,
        widget=forms.Select
    )

    сurrencie = forms.ModelChoiceField(
        label="Валюта",
        queryset=Currencies.objects.all(),
        required=False,
        widget=forms.Select
    )

    active = forms.BooleanField()
    comment = forms.CharField(widget=forms.Textarea(attrs={'cols': 10, 'rows': 4, 'class': 'form-control'}),
                              required=False, label="Комментарий")
