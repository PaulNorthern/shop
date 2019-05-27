from django.contrib import admin
from ecomapp.models import *


def make_payed(modeladmin, request, queryset):
    queryset.update(staus='Оплачено')
make_payed.short_description = "Пометить как оплаченные"


class OrderAdmin(admin.ModelAdmin):
    list_filter = ['staus']
    actions = [make_payed]

admin.site.register(Category)
admin.site.register(Brand)
admin.site.register(Product)
admin.site.register(CartItem)
admin.site.register(Cart)
admin.site.register(Order, OrderAdmin)
# Register your models here.
