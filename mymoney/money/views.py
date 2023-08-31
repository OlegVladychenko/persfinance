from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy

from django.views.generic import ListView, CreateView

from .forms import DocumentForm, DebitDocForm, CreditDocForm
from .models import *
import datetime


def index(request):
    return render(request, 'money/index.html')


class DocumentList(ListView):
    template_name = 'money/documents.html'

    def get_queryset(self, **kwargs):
        return Document.objects.all()


def show_doc(request, doc_id):
    doc = get_object_or_404(Document, pk=doc_id)
    doc_type = doc.type
    is_save = False
    if request.method == 'POST':
        if doc_type == 1:
            form = DebitDocForm(request.POST)

        elif doc_type == 2:
            form = CreditDocForm(request.POST)

        if form.is_valid():
            try:
                doc.date = form.cleaned_data.get('date')
                doc.sum = form.cleaned_data.get('sum')
                doc.sum_reg = form.cleaned_data.get('sum') * (-1)
                doc.counterparty = form.cleaned_data.get('counterparty')
                doc.category = form.cleaned_data.get('category')
                doc.сurrencie = form.cleaned_data.get('сurrencie')
                doc.account = form.cleaned_data.get('account')
                doc.active = form.cleaned_data.get('active')
                doc.comment = form.cleaned_data.get('comment')

                doc.save()
                is_save = True
                return redirect('docs')
            except:
                form.add_error(None, 'Ошибка добавления')
    else:

        if doc_type == 1:
            form = DebitDocForm()
        elif doc_type == 2:
            form = CreditDocForm()
        form.fields["date"].initial = doc.date
        form.fields["sum"].initial = doc.sum
        form.fields["sum_reg"].initial = doc.sum_reg
        form.fields["counterparty"].initial = doc.counterparty
        form.fields["category"].initial = doc.category
        form.fields["сurrencie"].initial = doc.сurrencie
        form.fields["account"].initial = doc.account
        form.fields["active"].initial = doc.active
        form.fields["comment"].initial = doc.comment

    context = {
        'doc_id': doc_id,
        'form': form,
    }

    return render(request, 'money/document.html', context)


def add_debit_doc(request):
    if request.method == 'POST':
        form = DebitDocForm(request.POST)
        if form.is_valid():
            try:
                form.cleaned_data["type"] = 1
                form.cleaned_data["sum_reg"] = form.cleaned_data["sum"]
                Document.objects.create(**form.cleaned_data)
                return redirect('docs')
            except Exception as e:
                form.add_error(None, str(e))
                print(str(e))
    else:
        form = DebitDocForm()
        form.fields["date"].initial = datetime.datetime.now()

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
                Document.objects.create(**form.cleaned_data)
                return redirect('docs')
            except Exception as e:
                form.add_error(None, str(e))
                print(str(e))
    else:
        form = CreditDocForm()
        form.fields["date"].initial = datetime.datetime.now()

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