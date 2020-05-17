from django.forms import ModelForm, ModelChoiceField
from .models import CartItem, Topping

class MenuForm(ModelForm):
    topping1 = ModelChoiceField(queryset=Topping.objects.all(), required=False, empty_label="Topping One")
    topping2 = ModelChoiceField(queryset=Topping.objects.all(), required=False, empty_label="Topping Two")
    topping3 = ModelChoiceField(queryset=Topping.objects.all(), required=False, empty_label="Topping Three")

    class Meta:
        model = CartItem
        fields = ['quantity', 'item', 'size', 'topping1', 'topping2', 'topping3']
