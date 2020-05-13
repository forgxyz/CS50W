from django.forms import ModelForm
from .models import CartItem, CartItemTopping

class MenuForm(ModelForm):
    class Meta:
        model = CartItem
        fields = ['quantity', 'item', 'size']


class ItemToppingForm(ModelForm):
    class Meta:
        model = CartItemTopping
        fields = ['topping']
