from django.urls import path

from .views import *

urlpatterns = [
    path('', index, name='home'),
    path('docs', DocumentList.as_view(), name='docs'),
    path('doc/<int:doc_id>', show_doc, name='show_doc'),
    path('add_debit_doc', add_debit_doc, name='add_debit_doc'),


]