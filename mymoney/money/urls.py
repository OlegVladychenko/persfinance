from django.urls import path

from .views import *

urlpatterns = [
    path('', index, name='home'),
    path('docs', DocumentList.as_view(), name='docs'),
    path('doc/<int:doc_id>', show_doc, name='show_doc'),
    path('add_debit_doc', add_debit_doc, name='add_debit_doc'),
    path('add_credit_doc', add_credit_doc, name='add_credit_doc'),
    path('delete_doc/<int:doc_id>/', delete_doc, name='delete_doc'),
    path('dirs', directories, name='dirs'),
    path('ctr_list', CounterpartyList.as_view(), name='ctr_list'),
    path('rates_list', ExchangeRatesList.as_view(), name='rates_list'),
    path('add_rate', AddExchangeRates.as_view(), name='add_rate'),
    path('show_rate/<int:rate_id>/', show_rate, name='show_rate'),
    path('delete_rate/<int:rate_id>/', delete_rate, name='delete_rate'),
    path('show_counterparty/<int:contr_id>/', show_counterparty, name='show_counterparty'),
    path('delete_counterparty/<int:contr_id>/', delete_counterparty, name='delete_counterparty'),
    path('add_counterparty', AddCounterpartyForm.as_view(), name='add_counterparty'),
    path('add_currencie', AddCurrencieForm.as_view(), name='add_currencie'),
    path('cur_list', CurrenciesList.as_view(), name='cur_list'),
    path('delete_currencie/<slug:curr_id>/', delete_currencie, name='delete_currencie'),
    path('show_currencie/<slug:curr_id>/', show_currencie, name='show_currencie'),



]