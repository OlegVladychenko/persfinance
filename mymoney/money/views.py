from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy

from django.views.generic import ListView, CreateView

from .forms import ExchangeRatesForm, DebitDocForm, CreditDocForm, CounterpartyForm, CurrencieForm, CategoryForm, MoneyAccountForm
from .models import *
from datetime import datetime, timedelta
from django.utils import timezone
from .utils import *


def index(request):
    account_sum_list = Document.objects.all() \
        .values('account__name', 'currencie__name') \
        .annotate(Sum('sum_reg')) \
        .filter(active=True)
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
    if request.method == 'POST':
        if doc_type == 1:
            form = DebitDocForm(request.POST)
            doc_name = "Приход"

        elif doc_type == 2:
            form = CreditDocForm(request.POST)
            doc_name = "Расход"

        if form.is_valid():
            try:
                doc.date = form.cleaned_data.get('date')
                doc.sum = form.cleaned_data.get('sum')

                doc.counterparty = form.cleaned_data.get('counterparty')
                doc.category = form.cleaned_data.get('category')
                doc.currencie = form.cleaned_data.get('currencie')
                doc.account = form.cleaned_data.get('account')
                doc.active = form.cleaned_data.get('active')
                doc.comment = form.cleaned_data.get('comment')
                reg_sum = get_regulated_sum(doc.date, doc.currencie, doc.sum)
                if doc_type == 1:
                    doc.sum_reg_val = reg_sum
                    doc.sum_reg = form.cleaned_data.get('sum')
                else:
                    doc.sum_reg_val = reg_sum * (-1)
                    doc.sum_reg = form.cleaned_data.get('sum') * (-1)
                doc.save()

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
                form.cleaned_data["sum_reg_val"] = get_regulated_sum(form.cleaned_data["date"],
                                                                     form.cleaned_data["currencie"],
                                                                     form.cleaned_data["sum"])

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
                form.cleaned_data["sum_reg_val"] = get_regulated_sum(form.cleaned_data["date"],
                                                                     form.cleaned_data["currencie"],
                                                                     form.cleaned_data["sum"]) * (-1)

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


def show_counterparty(request, contr_id):
    rate = get_object_or_404(Counterparty, pk=contr_id)
    if request.method == 'POST':
        form = CounterpartyForm(request.POST, instance=rate)
        if form.is_valid():
            form.save()
            return redirect('ctr_list')
    else:
        form = CounterpartyForm(instance=rate)

    context = {
        'contr_id': contr_id,
        'form': form,
    }
    return render(request, 'money/counterparty.html', context)


def delete_counterparty(request, contr_id):
    try:
        instance = Counterparty.objects.get(id=contr_id)
        instance.delete()
        return redirect('ctr_list')
    except:
        print('Ошибка удаления курса валют')
    return render(request)


class AddCounterpartyForm(DataMixin, CreateView):
    form_class = CounterpartyForm
    template_name = 'money/add_counterparty.html'
    success_url = reverse_lazy('ctr_list')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context()
        return dict(list(context.items()) + list(c_def.items()))


class AddCurrencieForm(DataMixin, CreateView):
    form_class = CurrencieForm
    template_name = 'money/add_currencie.html'
    success_url = reverse_lazy('cur_list')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context()
        return dict(list(context.items()) + list(c_def.items()))


class CurrenciesList(ListView):
    template_name = 'money/currencies.html'

    def get_queryset(self, **kwargs):
        return Currencies.objects.all()


def delete_currencie(request, curr_id):
    try:
        instance = Currencies.objects.get(code=curr_id)
        instance.delete()
        return redirect('cur_list')
    except:
        print('Ошибка удаления валюты')
    return render(request)


def show_currencie(request, curr_id):
    rate = get_object_or_404(Currencies, code=curr_id)
    if request.method == 'POST':
        form = CurrencieForm(request.POST, instance=rate)
        if form.is_valid():
            form.save()
            return redirect('cur_list')
    else:
        form = CurrencieForm(instance=rate)

    context = {
        'curr_id': curr_id,
        'form': form,
    }
    return render(request, 'money/currencie.html', context)


class CategoryList(ListView):
    template_name = 'money/categorys.html'

    def get_queryset(self, **kwargs):
        return Category.objects.all()


class AddCategoryForm(DataMixin, CreateView):
    form_class = CategoryForm
    template_name = 'money/add_category.html'
    success_url = reverse_lazy('category_list')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context()
        return dict(list(context.items()) + list(c_def.items()))


def show_category(request, category_id):
    rate = get_object_or_404(Category, pk=category_id)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=rate)
        if form.is_valid():
            form.save()
            return redirect('category_list')
    else:
        form = CategoryForm(instance=rate)

    context = {
        'category_id': category_id,
        'form': form,
    }
    return render(request, 'money/category.html', context)


def delete_category(request, category_id):
    try:
        instance = Category.objects.get(pk=category_id)
        instance.delete()
        return redirect('category_list')
    except:
        print('Ошибка удаления категории')
    return render(request)

class MoneyAccountList(ListView):
    template_name = 'money/moneyaccounts.html'

    def get_queryset(self, **kwargs):
        return MoneyAccount.objects.all()

class AddMoneyAccount(DataMixin, CreateView):
    form_class = MoneyAccountForm
    template_name = 'money/add_moneyaccount.html'
    success_url = reverse_lazy('monacn_list')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context()
        return dict(list(context.items()) + list(c_def.items()))

def show_money_account(request, monacc_id):
    money_account = get_object_or_404(MoneyAccount, pk=monacc_id)
    if request.method == 'POST':
        form = MoneyAccountForm(request.POST, instance=money_account)
        if form.is_valid():
            form.save()
            return redirect('monacn_list')
    else:
        form = MoneyAccountForm(instance=money_account)

    context = {
        'monacc_id': monacc_id,
        'form': form,
    }
    return render(request, 'money/moneyaccount.html', context)

def delete_monacc(request, monacc_id):
    try:
        instance = MoneyAccount.objects.get(pk=monacc_id)
        instance.delete()
        return redirect('monacn_list')
    except:
        print('Ошибка удаления аккаунт')
    return render(request)