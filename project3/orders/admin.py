from django.contrib import admin

from .models import Item, Topping, Cart, CartItem, Order, OrderItem
# Register your models here.
admin.site.register(Item)
admin.site.register(Topping)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Order)
admin.site.register(OrderItem)
