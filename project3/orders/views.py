from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

from .models import Item, Topping, Cart, CartItem

# Create your views here.
def cart(request):
    # get items from form submission
    items = {}
    total = 0
    user = User.objects.get(pk=request.user.id)
    for record in Item.objects.all():
        try:
            items[record.item] = request.POST[record.item]
        except:
            pass
    # create cart record
    cart = Cart(userID=user, total=total)
    cart.save()
    # add items to associated cart
    for item, size in items.items():
        record = Item.objects.get(item=item)
        price = record.priceSm if size == 'Small' else record.priceLg
        total += price
        a = CartItem(cartID=cart, itemID=record, toppingID=None, size=size, price=price)
        a.save()
    cart.total = total
    cart.save()
    context = {"selections": items}
    return render(request, "orders/success.html", context)


def clear_cart(request):
    user = User.objects.get(pk=request.user.id)
    try:
        Cart.objects.get(userID=user).delete()
        message = "Cart successfully deleted."
    except:
        message = "No cart to delete."
    context = {"message": message, "items": Item.objects.all(), "toppings": Topping.objects.all()}
    return render(request, "orders/menu.html", context)

def index(request):
    if request.user.is_authenticated:
        # if logged in, load menu for display
        context = {"items": Item.objects.all(), "toppings": Topping.objects.all()}
        return render(request, "orders/menu.html", context)
    context = {"status": "not logged in"}
    return render(request, "orders/index.html", context)


# just pass request. get form data with request.POST["input name"]
# remember to not duplicate local function names w django functions
def ulogin(request):
    username = request.POST["username"]
    password = request.POST["password"]
    user = authenticate(request, username=username, password=password)
    if user:
        login(request, user)
        return HttpResponseRedirect("/")
    return render(request, "orders/failure.html")


def ulogout(request):
    logout(request)
    return HttpResponseRedirect("/")


def uregister(request):
    username = request.POST["username"]
    password = request.POST["password"]
    user = User.objects.create_user(username, password=password)
    context = {"username": username}
    return render(request, "orders/success.html", context)
