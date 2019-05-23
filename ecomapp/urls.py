from django.conf.urls import url, include
from django.urls import path
from ecomapp.views import *

urlpatterns = [
    path('remove_from_cart/', remove_from_cart_view, name = 'remove_from_cart'),
    path('category/<str:category_slug>/', category_view, name='category_detail'),
    path('product/<str:product_slug>/', product_view, name='product_detail'),
    path('cart/', cart_view, name='cart'),
    path('add_to_cart/', add_to_cart_view, name = 'add_to_cart'),
    path('change_item_qty', change_item_qty, name="change_item_qty"),
    url(r'^$', base_view, name='base'), # ^ - начало адрес и $ - конец адреса
  
]
