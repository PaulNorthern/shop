from django.conf.urls import url, include
from ecomapp.views import *

urlpatterns = [
    url('', base_view, name='base'),
  
]
