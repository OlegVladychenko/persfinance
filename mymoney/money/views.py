from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404

from django.views.generic import ListView, CreateView
from .models import *

def index(request):
    return render(request, 'money/index.html')


class DocumentList(ListView):
    template_name = 'money/documents.html'

    def get_queryset(self, **kwargs):
        return Document.objects.all()

def show_doc(request, doc_id):
    doc = get_object_or_404(Document, pk=doc_id)
    print(request.method)
    return render(request, 'money/document.html')
