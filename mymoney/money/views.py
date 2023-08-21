from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy

from django.views.generic import ListView, CreateView

from .forms import DocumentForm, AddDebitDocForm, AddCreditDocForm
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
    print(request.method)
    if request.method == 'POST':
        form = DocumentForm(request.POST, instance=doc)
        if form.is_valid():
            try:
                form.save()
            except:
                form.add_error(None, 'Ошибка добавления')
    else:
        form = DocumentForm(instance=doc)

    context = {
        'doc_id': doc_id,
        'form': form,
    }
    return render(request, 'money/document.html', context)


def add_debit_doc(request):
    if request.method == 'POST':
        form = AddDebitDocForm(request.POST)
        if form.is_valid():
            try:
                form.cleaned_data["type"] = 1
                form.cleaned_data["sum_reg"] = form.cleaned_data["sum"]
                Document.objects.create(**form.cleaned_data)
                return redirect('docs')
            except Exception as e:
                form.add_error(None,  str(e))
                print(str(e))
    else:
        form = AddDebitDocForm()
        form.fields["date"].initial = datetime.datetime.now()

    context = {
        'form': form
    }
    return render(request, 'money/add_debit.html', context)

def add_credit_doc(request):
    if request.method == 'POST':
        form = AddCreditDocForm(request.POST)
        if form.is_valid():
            try:
                form.cleaned_data["type"] = 2
                form.cleaned_data["sum_reg"] = form.cleaned_data["sum"] * (-1)
                Document.objects.create(**form.cleaned_data)
                return redirect('docs')
            except Exception as e:
                form.add_error(None,  str(e))
                print(str(e))
    else:
        form = AddCreditDocForm()
        form.fields["date"].initial = datetime.datetime.now()

    context = {
        'form': form
    }
    return render(request, 'money/add_credit.html', context)
