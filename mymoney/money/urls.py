from django.urls import path

from .views import *

urlpatterns = [
    #path('', index),
    path('', DocumentList.as_view(), name='documents'),

]