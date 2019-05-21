from django.shortcuts import render
#вся бизнес-логика в котороый будет выборка из БД для вывода в шаблон
# Create your views here.
from ecomapp.models import *
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse

def base_view(request):
    try:
        cart_id = request.session['cart_id']
        cart = Cart.objects.get(id=cart_id)
        request.session['total'] = cart.items.count()
    except:
        cart = Cart()
        cart.save()
        cart_id = cart.id
        request.session['cart_id'] = cart_id
        cart = Cart.objects.get(id=cart_id)
    categories = Category.objects.all()
    products = Product.objects.all()
    context = {
        'categories': categories,
        'products': products,
        'cart' : cart 
        
    }
    return render(request, 'base.html', context)

def product_view(request, product_slug): #получать по слагу-продукта
    try:
        cart_id = request.session['cart_id']
        cart = Cart.objects.get(id=cart_id)
        request.session['total'] = cart.items.count()
    except:
        cart = Cart()
        cart.save()
        cart_id = cart.id # присваиваем id новой созданной корзины
        request.session['cart_id'] = cart_id
        cart = Cart.objects.get(id=cart_id)

    product = Product.objects.get(slug=product_slug)
    categories = Category.objects.all() # для отображения категорий в выпадающем списке
    context = {
        'product' : product,
        'categories' : categories,
        'cart' : cart 
    }
    return render(request, 'product.html', context) # передаем информацию этого объекта на шаблон

def category_view(request, category_slug): #получать по слагу-категории
    category = Category.objects.get(slug=category_slug)
    products_of_category = Product.objects.filter(category=category) # из строчки выше берем объекты категории и сравниваем
    context = {                                                      # с моделью Product
        'category' : category,
        'products_of_category': products_of_category,
    }
    return render(request, 'category.html', context)

def cart_view(request):
    try:
        cart_id = request.session['cart_id']
        cart = Cart.objects.get(id=cart_id)
        request.session['total'] = cart.items.count()
    except:
        cart = Cart()
        cart.save()
        cart_id = cart.id
        request.session['cart_id'] = cart_id
        cart = Cart.objects.get(id=cart_id)
    context = {
        'cart' : cart
    }
    return render(request, 'cart.html', context)

def add_to_cart_view(request):
    try:
        cart_id = request.session['cart_id']
        cart = Cart.objects.get(id=cart_id)
        request.session['total'] = cart.items.count()
    except:
        cart = Cart()
        cart.save()
        cart_id = cart.id
        request.session['cart_id'] = cart_id
        cart = Cart.objects.get(id=cart_id)
    product_slug = request.GET.get('product_slug')
    product = Product.objects.get(slug=product_slug)
    cart.add_to_cart(product.slug)
    return JsonResponse({'cart_total': cart.items.count()})

def remove_from_cart_view(request):
    try:
        cart_id = request.session['cart_id']
        cart = Cart.objects.get(id=cart_id)
        request.session['total'] = cart.items.count()
    except:
        cart = Cart()
        cart.save()
        cart_id = cart.id
        request.session['cart_id'] = cart_id
        cart = Cart.objects.get(id=cart_id)
    product_slug = request.GET.get('product_slug')
    product = Product.objects.get(slug=product_slug)
    cart.remove_from_cart(product.slug)
    return JsonResponse({'cart_total': cart.items.count()})
