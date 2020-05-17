from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse

import decimal

from .models import Item, Topping, Cart, CartItem, Order, OrderItem
from .forms import MenuForm

# Create your views here.
def index(request):
    if request.user.is_authenticated:
        # if logged in, load menu for display
        return HttpResponseRedirect("menu")
    return render(request, "orders/index.html")


# load cart form (GET) or handle add-to-cart submisison (POST)
def cart(request):
    context = {'cart': [], 'additions': []}
    user = User.objects.get(pk=request.user.id)
    try:
        cart = Cart.objects.get(user=user)
    except:
        cart = False

    if request.method == 'POST':
    # order submission, add to cart
        # bind data to the form
        form = MenuForm(request.POST)
        if form.is_valid():
            # process data here
            item = Item.objects.get(item=form.cleaned_data['item'])
            size = form.cleaned_data['size']
            quantity = form.cleaned_data['quantity']
            price = item.priceSm if size == "Small" else item.priceLg
            total = decimal.Decimal(quantity * price)
            topping1 = form.cleaned_data['topping1']
            topping2 = form.cleaned_data['topping2']
            topping3 = form.cleaned_data['topping3']

            # get existing cart or create a new cart object
            if not cart:
                cart = Cart(user=user)
            cart.total += total
            cart.save()

            # add items to the cart
            a = CartItem(cart=cart, item=item, size=size, quantity=quantity, topping1=topping1, topping2=topping2, topping3=topping3)
            a.save()

            context['additions'].append(a)

    if cart:
        for record in CartItem.objects.filter(cart=cart).all():
            context['cart'].append(record)
        context['total'] = cart.total
    # load menu
    form = MenuForm()
    context['form'] = form
    return render(request, "orders/menu.html", context)


# empty user's cart
def clear_cart(request):
    user = User.objects.get(pk=request.user.id)
    try:
        Cart.objects.get(user=user).delete()
        message = "Cart successfully deleted."
    except:
        message = "No cart to delete."
    context = {"message": message}
    return HttpResponseRedirect(reverse("cart"))


def order(request):
    user = User.objects.get(pk=request.user.id)
    # get current cart
    cart = Cart.objects.get(user=user)
    # create order record
    order = Order(user=user, total=cart.total)
    order.save()

    for record in CartItem.objects.filter(cart=cart):
        a = OrderItem(order=order, item=record.item, size=record.size, quantity=record.quantity, topping1=record.topping1, topping2=record.topping2, topping3=record.topping3)
        a.save()

    cart.delete()
    return render(request, "orders/success.html")


# user account related views
def ulogin(request):
    username = request.POST["username"]
    password = request.POST["password"]
    user = authenticate(request, username=username, password=password)
    if user:
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    return render(request, "orders/failure.html")


def ulogout(request):
    logout(request)
    return HttpResponseRedirect("/")


def uregister(request):
    username = request.POST["username"]
    password = request.POST["password"]
    # handle exception if username exists
    user = User.objects.create_user(username, password=password)
    login(request, user)
    return HttpResponseRedirect(reverse("index"))
