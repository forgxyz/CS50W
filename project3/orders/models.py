from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator

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
    size = models.CharField(max_length=7, choices=SIZES)
    quantity = models.IntegerField(default=1, validators=[MinValueValidator(1)])
    topping1 = models.ForeignKey(Topping, on_delete=models.CASCADE, null=True, related_name='topping1')
    topping2 = models.ForeignKey(Topping, on_delete=models.CASCADE, null=True, related_name='topping2')
    topping3 = models.ForeignKey(Topping, on_delete=models.CASCADE, null=True, related_name='topping3')


    def __str__(self):
        return f"{self.quantity} {self.size} {self.item}"


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total = models.DecimalField(max_digits=8, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.user}'s order"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    size = models.CharField(max_length=7, choices=SIZES)
    quantity = models.IntegerField(default=1, validators=[MinValueValidator(1)])
    topping1 = models.ForeignKey(Topping, on_delete=models.CASCADE, null=True, related_name='otopping1')
    topping2 = models.ForeignKey(Topping, on_delete=models.CASCADE, null=True, related_name='otopping2')
    topping3 = models.ForeignKey(Topping, on_delete=models.CASCADE, null=True, related_name='otopping3')


    def __str__(self):
        return f"{self.quantity} {self.size} {self.item}"
