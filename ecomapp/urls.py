from django.conf.urls import url, include
from django.urls import path
from ecomapp.views import *

urlpatterns = [
    path('category/<str:category_slug>/', category_view, name='category_detail'),
    path('product/<str:product_slug>/', product_view, name='product_detail'),
    path('cart/', cart_view, name='cart'),
    path('add_to_cart/<str:product_slug>', add_to_cart_view, name = 'add_to_cart'),
    url(r'^$', base_view, name='base'), # ^ - начало адрес и $ - конец адреса
  
]
