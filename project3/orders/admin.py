from django.contrib import admin

from .models import Items, Toppings, Orders, OrderItems
# Register your models here.
admin.site.register(Items)
admin.site.register(Toppings)
admin.site.register(Orders)
admin.site.register(OrderItems)
