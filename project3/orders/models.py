from django.db import models
from django.contrib.auth.models import User

# Create your models here.
# change to singular... Django adds the s
class Item(models.Model):
    item = models.CharField(max_length = 50)
    priceSm = models.DecimalField(max_digits=5, decimal_places=2)
    priceLg = models.DecimalField(max_digits=5, decimal_places=2)
    category = models.CharField(max_length=20)
    topping = models.BooleanField(default=False)

    def __str__(self):
        return self.item


class Topping(models.Model):
    topping = models.CharField(max_length = 25)

    def __str__(self):
        return self.topping


class Order(models.Model):
    userID = models.ForeignKey(User, on_delete=models.CASCADE)
    total = models.DecimalField(max_digits=8, decimal_places=2)
    timestamp = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{name} - {timestamp}"


class OrderItem(models.Model):
    orderID = models.ForeignKey(Order, on_delete=models.CASCADE)
    itemID = models.ForeignKey(Item, on_delete=models.CASCADE)
    toppingID = models.ForeignKey(Topping, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{orderID} {itemID} {toppingID}"


class Cart(models.Model):
    userID = models.ForeignKey(User, on_delete=models.CASCADE, unique=True)
    total = models.DecimalField(max_digits=8, decimal_places=2)


class CartItem(models.Model):
    cartID = models.ForeignKey(Cart, on_delete=models.CASCADE)
    itemID = models.ForeignKey(Item, on_delete=models.CASCADE)
    toppingID = models.ForeignKey(Topping, on_delete=models.CASCADE, null=True)
