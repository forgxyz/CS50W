from django.db import models

# Create your models here.
# change to singular... Django adds the s
class Items(models.Model):
    item = models.CharField(max_length = 50)
    priceSm = models.DecimalField(max_digits=5, decimal_places=2)
    priceLg = models.DecimalField(max_digits=5, decimal_places=2)
    category = models.CharField(max_length=20)

    def __str__(self):
        return self.item


class Toppings(models.Model):
    topping = models.CharField(max_length = 25)

    def __str__(self):
        return self.topping


class Orders(models.Model):
    name = models.CharField(max_length = 50)
    total = models.DecimalField(max_digits=8, decimal_places=2)
    timestamp = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{name} - {timestamp}"


class OrderItems(models.Model):
    orderID = models.ForeignKey(Orders, on_delete=models.CASCADE)
    itemID = models.ForeignKey(Items, on_delete=models.CASCADE)
    toppingID = models.ForeignKey(Toppings, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{orderID} {itemID} {toppingID}"
