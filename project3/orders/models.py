from django.db import models
from django.contrib.auth.models import User


SIZES = [
    ('Small', 'Small'),
    ('Large', 'Large'),
]

class Item(models.Model):
    item = models.CharField(max_length = 50)
    priceSm = models.DecimalField(max_digits=5, decimal_places=2)
    priceLg = models.DecimalField(max_digits=5, decimal_places=2)
    category = models.CharField(max_length=20)
    topping = models.IntegerField()

    def __str__(self):
        return self.item


class Topping(models.Model):
    topping = models.CharField(max_length = 25)

    def __str__(self):
        return self.topping


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, unique=True)
    total = models.DecimalField(max_digits=8, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.user}'s cart"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    topping = models.BooleanField(default=False)
    size = models.CharField(max_length=7, choices=SIZES)
    quantity = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.quantity} {self.size} {self.item}"


class CartItemTopping(models.Model):
    cartitem = models.ForeignKey(CartItem, on_delete=models.CASCADE)
    topping = models.ForeignKey(Topping, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.topping} on {self.cartitem}"
