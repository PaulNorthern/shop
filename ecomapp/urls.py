from django.conf.urls import url, include
from django.urls import path
from ecomapp.views import *
from django.views.generic import TemplateView 

urlpatterns = [
    path('remove_from_cart/', remove_from_cart_view, name = 'remove_from_cart'),
    path('category/<str:category_slug>/', category_view, name='category_detail'),
    path('product/<str:product_slug>/', product_view, name='product_detail'),
    path('cart/', cart_view, name='cart'),
    path('add_to_cart/', add_to_cart_view, name = 'add_to_cart'),
    path('change_item_qty/', change_item_qty, name="change_item_qty"),
    path('checkout/', checkout_view, name='checkout'),
    path('order/', order_create_view, name='create_order'),
    path('make_order/', make_order_view, name = 'make_order'),
    path('thank_you/', TemplateView.as_view(template_name='thank_you.html'), name='thank_you'),
    path('account', account_view, name='account'),
    path('registration/', registration_view, name="registration"),
    path('login/', login_view, name="login"),
    url(r'^$', base_view, name='base'), # ^ - начало адрес и $ - конец адреса
  
]
