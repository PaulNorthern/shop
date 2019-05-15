from django.shortcuts import render
#вся бизнес-логика в котороый будет выборка из БД для вывода в шаблон
# Create your views here.
from ecomapp.models import *

def base_view(request):
    categories = Category.objects.all()
    products = Product.objects.all()
    context = {
        'categories': categories,
        'products': products
    }

    return render(request, 'base.html', context)