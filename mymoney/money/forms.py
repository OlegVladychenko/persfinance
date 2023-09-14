from django import forms

from .models import *


class DateInput(forms.DateInput):
    input_type = 'date'


class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = "__all__"
        #fields = ['id','date', 'type', 'sum', 'sum_reg', 'counterparty', 'category', 'currencie', 'account', 'active', 'comment']
        widgets = {
            'id': forms.TextInput(attrs={'class': 'form-control'}),
            'type': forms.IntegerField(required=False),
           # 'counterparty': forms.TextInput(attrs={'class': 'form-control'}),
            # 'category': forms.TextInput(attrs={'class': 'form-control'}),
            #'currencie': forms.TextInput(attrs={'class': 'form-control'}),
            #'account': forms.TextInput(attrs={'class': 'form-control'}),
            #'active': forms.TextInput(attrs={'class': 'form-control'}),
            #'comment': forms.TextInput(attrs={'class': 'form-control'})
        }
        labels = {
            'id': 'Заголовок',
            'sum': 'Сумма',
        }


class DebitDocForm(forms.Form):
    date = forms.DateField(widget=DateInput(attrs={'class': 'form-control'}), label="Дата")
    type = forms.IntegerField(required=False)
    sum = forms.DecimalField(widget=forms.TextInput(attrs={'class': 'form-control'}), label="Сумма")
    sum_reg = forms.DecimalField(widget=forms.TextInput(attrs={'class': 'form-control'}),required=False)
    sum_reg_val = forms.DecimalField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)

    counterparty = forms.ModelChoiceField(
        label="Контрагент",
        queryset=Counterparty.objects.all(),
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    category = forms.ModelChoiceField(
        label="Категория",
        queryset=Category.objects.all(),
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    currencie = forms.ModelChoiceField(
        label="Валюта",
        queryset=Currencies.objects.all(),
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    account = forms.ModelChoiceField(
        label="Счет/Касса",
        queryset=MoneyAccount.objects.all(),
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    active = forms.BooleanField(widget=forms.CheckboxInput(attrs={'class': 'form-check-input','type':'checkbox'}), label="Ативно", required=False)
    comment = forms.CharField(widget=forms.Textarea(attrs={'cols': 8, 'rows': 4, 'class': 'form-control'}),
                              required=False, label="Комментарий")

class CreditDocForm(forms.Form):
    date = forms.DateField(widget=DateInput(attrs={'class': 'form-control'}), label="Дата")
    type = forms.IntegerField(required=False)
    sum = forms.DecimalField(widget=forms.TextInput(attrs={'class': 'form-control'}), label="Сумма")
    sum_reg = forms.DecimalField(widget=forms.TextInput(attrs={'class': 'form-control'}),required=False)
    sum_reg_val = forms.DecimalField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)

    counterparty = forms.ModelChoiceField(
        label="Контрагент",
        queryset=Counterparty.objects.all(),
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    category = forms.ModelChoiceField(
        label="Категория",
        queryset=Category.objects.all(),
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    currencie = forms.ModelChoiceField(
        label="Валюта",
        queryset=Currencies.objects.all(),
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    account = forms.ModelChoiceField(
        label="Счет/Касса",
        queryset=MoneyAccount.objects.all(),
        widget=forms.Select(attrs={'class': 'form-select'})
    )


    active = forms.BooleanField(widget=forms.CheckboxInput(attrs={'class': 'form-check-input','type':'checkbox'}), label="Ативно", required=False)
    comment = forms.CharField(widget=forms.Textarea(attrs={'cols': 8, 'rows': 4, 'class': 'form-control'}),
                              required=False, label="Комментарий")