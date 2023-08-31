from django.urls import path

from .views import *

urlpatterns = [
    path('', index, name='home'),
    path('docs', DocumentList.as_view(), name='docs'),
    path('doc/<int:doc_id>', show_doc, name='show_doc'),
    path('add_debit_doc', add_debit_doc, name='add_debit_doc'),
    path('add_credit_doc', add_credit_doc, name='add_credit_doc'),
    path('delete_doc/<int:doc_id>/', delete_doc, name='delete_doc'),


]