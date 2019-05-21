from django.shortcuts import render
#вся бизнес-логика в котороый будет выборка из БД для вывода в шаблон
# Create your views here.
from ecomapp.models import *
from django.http import HttpResponseRedirect

def base_view(request):
    try:
        cart_id = request.session['card_id']
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
        cart_id = request.session['card_id']
        cart = Cart.objects.get(id=cart_id)
        request.session['total'] = cart.items.count()
    except:
        cart = Cart()
        cart.save()
        cart_id = cart.id
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
        cart_id = request.session['card_id']
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

def add_to_cart_view(request, product_slug):
    try:
        cart_id = request.session['card_id']
        cart = Cart.objects.get(id=cart_id)
        request.session['total'] = cart.items.count()
    except:
        cart = Cart()
        cart.save()
        cart_id = cart.id
        request.session['cart_id'] = cart_id
        cart = Cart.objects.get(id=cart_id)
    product = Product.objects.get(slug=product_slug)
    new_item, _ = CartItem.objects.get_or_create(product=product, item_total=product.price)    
    if new_item not in cart.items.all():
        cart.items.add(new_item)
        cart.save()
        return HttpResponseRedirect('/cart/')
