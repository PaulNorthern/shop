from django.db import models
from django.db.models.signals import pre_save
from django.utils.text import slugify
#slugify - берет поле name и превращает его в slug, для валидации
from transliterate import translit
from django.urls import reverse #для создания ссылок на объекты


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