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

def product_view(request, product_slug): #получать по слагу-продукта
    product = Product.objects.get(slug=product_slug)
    categories = Category.objects.all() # для отображения категорий в выпадающем списке
    context = {
        'product' : product,
        'categories' : categories
    }
    return render(request, 'product.html', context) # передаем информацию этого объекта на шаблон

def category_view(request, category_slug): #получать по слагу-категории
    category = Category.objects.get(slug=category_slug)
    categories = Category.objects.all() # для отображения категорий в выпадающем списке
    products_of_category = Product.objects.filter(category=category) # из строчки выше берем объекты категории и сравниваем
    context = {                                                      # с моделью Product
        'category' : category,
        'products_of_category': products_of_category,
        'categories' : categories
    }
    return render(request, 'category.html', context)