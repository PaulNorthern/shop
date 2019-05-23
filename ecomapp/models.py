from django.db import models
from django.db.models.signals import pre_save
from django.utils.text import slugify
#slugify - берет поле name и превращает его в slug, для валидации
from transliterate import translit
from django.urls import reverse #для создания ссылок на объекты
from decimal import Decimal


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):#название метода - это соглашение Джанги
        return reverse('category_detail', kwargs={'category_slug': self.slug})

# sender - это модель объекта которую буду сохрнаять
def pre_save_category_slug(sender, instance, *args, **kwargs): # генерация slug'a
    #заполнен ли slug?
    if not instance.slug:
        slug = slugify(translit(str(instance.name), reversed=True)) # reversed для первода русскоязычного названия в транслит
        instance.slug = slug 

#нужно соединить сигнал с моделью
pre_save.connect(pre_save_category_slug, sender=Category)

class Brand(models.Model):
    name = models.CharField(max_length=100)
 
    def __str__(self):
        return self.name


def image_folder(instance, filename): #для сохр. изображения
    filename = instance.slug + '.' + filename.split('.')[1] #slug + расширение
    return "{0}/{1}".format(instance.slug, filename) #сохраняем в папку под SLUG и картинку в ней под slug.png

class ProductManager(models.Manager): # переопределил базовый менеджер, чтобы отображалиьс доступные товары
    def all(self, *args, **kwargs):
        return super(ProductManager, self).get_queryset().filter(available=True)

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE) # у 1 товара = 1 категория
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE,) #тоже с брендом
    title = models.CharField(max_length=120)
    slug = models.SlugField()
    description = models.TextField()
    image = models.ImageField(upload_to=image_folder)
    price = models.DecimalField(max_digits=9, decimal_places=2) #цифр после ,
    available = models.BooleanField(default=True)
    objects = ProductManager()

    def __str__(self):
        return self.title 

    def get_absolute_url(self): #reverse будет генерить нам ссылку
        return reverse('product_detail', kwargs={'product_slug': self.slug})

class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    qty = models.PositiveIntegerField(default=1) # кол-во
    item_total = models.DecimalField(max_digits=9, decimal_places=2, default=0.00) # менять кол-во предеметов

    def __str__(self):
        return "Cart item for product {0}".format(self.product.title)

class Cart(models.Model):
    items = models.ManyToManyField(CartItem, blank=True) # в корзину много предметов
    cart_total = models.DecimalField(max_digits=9, decimal_places=2, default = 0.00) # итоговая сумма    

    def __str__(self):
        return  str(self.id)
    
    def add_to_cart(self, product_slug):
        cart = self
        product = Product.objects.get(slug=product_slug)
        new_item, _ = CartItem.objects.get_or_create(product=product, item_total=product.price)       
        if new_item not in cart.items.all():
            cart.items.add(new_item)
            cart.save()
    
    def remove_from_cart(self, product_slug):
        cart = self
        product = Product.objects.get(slug=product_slug)
        for cart_item in cart.items.all():
            if cart_item.product == product:
                cart.items.remove(cart_item)
                cart.save()

    def change_qty(self, qty, item_id):
        cart = self
        cart_item = CartItem.objects.get(id=int(item_id))
        cart_item.qty = int(qty)
        cart_item.item_total = int(qty) * Decimal(cart_item.product.price)
        cart_item.save()
        new_cart_total = 0.00
        for item in cart.items.all():
            new_cart_total += float(item.item_total)
        cart.cart_total = new_cart_total
        cart.save()


ORDER_STATUS_CHOICES = {
    ('Принят в обработку', ' Принят в обработку'), ('Выполняется', 'Выполняется'), ('Оплачено', 'Оплачено')
}

# class Order(models.Model):
#     user = 
