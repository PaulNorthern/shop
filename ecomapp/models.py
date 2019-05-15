from django.db import models
from django.db.models.signals import pre_save
from django.utils.text import slugify
#slugify - берет поле name и превращает его в slug, для валидации
from transliterate import translit


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(blank=True)

    def __str__(self):
        return self.name

# sender - это модель объекта которую буду сохрнаять
def pre_save_category_slug(sender, instance, *args, **kwargs): # генерация slug'a
    #заполнен ли slug?
    if not instance.slug:
        slug = slugify(translit(str(instance.name)))
        instance.slug = slug 

#нужно соединить сигнал с моделью
pre_save.connect(pre_save_category_slug, sender=Category)

class Brand(models.Model):
    name = models.CharField(max_length=100)
 
    def __str__(self):
        return self.name


def image_folder(instance, filename): #для сохр. изображения
    filename = instance.slug + '.' + filename.split('.')[1] #slug + расширение
    return "{0}/{1}".format(instance.slug, filename)


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE) # у 1 товара = 1 категория
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE,) #тоже с брендом
    title = models.CharField(max_length=120)
    slug = models.SlugField()
    description = models.TextField()
    image = models.ImageField(upload_to=image_folder)
    price = models.DecimalField(max_digits=9, decimal_places=2) #цифр после ,
    available = models.BooleanField(default=True)

    def __str__(self):
        return self.title 