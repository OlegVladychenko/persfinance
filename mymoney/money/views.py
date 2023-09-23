from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy

from django.views.generic import ListView, CreateView

from .forms import ExchangeRatesForm, DebitDocForm, CreditDocForm
from .models import *
from datetime import datetime, timedelta
from django.utils import timezone
from .utils import *


def index(request):
    account_sum_list = Document.objects.all() \
        .values('account__name', 'currencie__name') \
        .annotate(Sum('sum_reg')) \
        .filter(active=True)
    print(account_sum_list)
    context = {
        'data_list': account_sum_list
    }

    return render(request, 'money/index.html', context)


class DocumentList(ListView):
    template_name = 'money/documents.html'

    def get_queryset(self, **kwargs):
        return Document.objects.all()


def show_doc(request, doc_id):
    doc = get_object_or_404(Document, pk=doc_id)

    doc_type = doc.type
    doc_name = ""
    is_save = False
    if request.method == 'POST':
        if doc_type == 1:
            form = DebitDocForm(request.POST)
            doc_name = "Приход"

        elif doc_type == 2:
            form = CreditDocForm(request.POST)
            doc_name = "Расход"

        if form.is_valid():
            print(form.cleaned_data)
            try:
                doc.date = form.cleaned_data.get('date')
                doc.sum = form.cleaned_data.get('sum')
                doc.sum_reg = form.cleaned_data.get('sum') * (-1)
                doc.counterparty = form.cleaned_data.get('counterparty')
                doc.category = form.cleaned_data.get('category')
                doc.currencie = form.cleaned_data.get('currencie')
                doc.account = form.cleaned_data.get('account')
                doc.active = form.cleaned_data.get('active')
                doc.comment = form.cleaned_data.get('comment')
                doc.sum_reg_val = form.cleaned_data.get('sum') * (-1)

                doc.save()
                is_save = True
                return redirect('docs')
            except:
                form.add_error(None, 'Ошибка добавления')
    else:

        if doc_type == 1:
            form = DebitDocForm()
            doc_name = "Приход"
        elif doc_type == 2:
            form = CreditDocForm()
            doc_name = "Расход"
        form.fields["date"].initial = doc.date
        form.fields["sum"].initial = doc.sum
        form.fields["sum_reg"].initial = doc.sum_reg
        form.fields["counterparty"].initial = doc.counterparty
        form.fields["category"].initial = doc.category
        form.fields["currencie"].initial = doc.currencie
        form.fields["account"].initial = doc.account
        form.fields["active"].initial = doc.active
        form.fields["comment"].initial = doc.comment
        form.fields["sum_reg_val"].initial = doc.sum_reg_val

    context = {
        'doc_id': doc_id,
        'form': form,
        'doc_name': doc_name
    }

    return render(request, 'money/document.html', context)


def add_debit_doc(request):
    if request.method == 'POST':
        form = DebitDocForm(request.POST)
        if form.is_valid():
            try:
                form.cleaned_data["type"] = 1
                form.cleaned_data["sum_reg"] = form.cleaned_data["sum"]
                form.cleaned_data["sum_reg_val"] = form.cleaned_data.get('sum')
                Document.objects.create(**form.cleaned_data)
                return redirect('docs')
            except Exception as e:
                form.add_error(None, str(e))
                print(str(e))
    else:
        form = DebitDocForm()
        form.fields["date"].initial = timezone.now().date()

    context = {
        'form': form
    }
    return render(request, 'money/add_debit.html', context)


def add_credit_doc(request):
    if request.method == 'POST':
        form = CreditDocForm(request.POST)
        if form.is_valid():
            try:
                form.cleaned_data["type"] = 2
                form.cleaned_data["sum_reg"] = form.cleaned_data["sum"] * (-1)
                form.cleaned_data["sum_reg_val"] = form.cleaned_data.get('sum') * (-1)
                Document.objects.create(**form.cleaned_data)
                return redirect('docs')
            except Exception as e:
                form.add_error(None, str(e))
                print(str(e))
    else:
        form = CreditDocForm()
        form.fields["date"].initial = timezone.now().date()

    context = {
        'form': form
    }
    return render(request, 'money/add_credit.html', context)


def delete_doc(request, doc_id):
    try:
        instance = Document.objects.get(id=doc_id)
        instance.delete()
        return redirect('docs')
    except:
        print('Ошибка удаления документа')
    return render(request)


def directories(request):
    return render(request, 'money/directories.html')


class CounterpartyList(ListView):
    template_name = 'money/counterpartys.html'

    def get_queryset(self, **kwargs):
        return Counterparty.objects.all()


class ExchangeRatesList(ListView):
    template_name = 'money/exchangerates.html'

    def get_queryset(self, **kwargs):
        return ExchangeRates.objects.all()


class AddExchangeRates(DataMixin, CreateView):
    form_class = ExchangeRatesForm
    template_name = 'money/add_rate.html'
    success_url = reverse_lazy('rates_list')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context()
        return dict(list(context.items()) + list(c_def.items()))


def show_rate(request, rate_id):
    rate = get_object_or_404(ExchangeRates, pk=rate_id)
    if request.method == 'POST':
        form = ExchangeRatesForm(request.POST, instance=rate)
        if form.is_valid():
            form.save()
            return redirect('rates_list')
    else:
        form = ExchangeRatesForm(instance=rate)

    context = {
        'rate_id': rate_id,
        'form': form,
    }
    return render(request, 'money/rate.html', context)


def delete_rate(request, rate_id):
    try:
        instance = ExchangeRates.objects.get(id=rate_id)
        instance.delete()
        return redirect('rates_list')
    except:
        print('Ошибка удаления курса валют')
    return render(request)
