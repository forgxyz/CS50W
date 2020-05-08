from django.contrib import admin

from .models import Item, Topping, Order, OrderItem, Cart, CartItem
# Register your models here.
admin.site.register(Item)
admin.site.register(Topping)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Cart)
admin.site.register(CartItem)
