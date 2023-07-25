from django.http import HttpResponse
from django.shortcuts import render

from django.views.generic import ListView, CreateView
from .models import *


def index(request):
    return HttpResponse('hi')

class DocumentList(ListView):
    template_name = 'money/documents.html'

    def get_queryset(self, **kwargs):
        return Document.objects.all()
