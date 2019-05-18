from django.conf.urls import url, include
from django.urls import path
from ecomapp.views import *

urlpatterns = [
    path('category/<str:category_slug>/', category_view, name='category_detail'),
    path('product/<str:product_slug>/', product_view, name='product_detail'),
    url(r'^$', base_view, name='base'), # ^ - начало адрес и $ - конец адреса
  
]
