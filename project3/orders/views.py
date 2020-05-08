from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

from .models import Item, Topping

# Create your views here.
def index(request):
    if request.user.is_authenticated:
        # if logged in, load menu for display
        context = {"items": Item.objects.all(), "toppings": Topping.objects.all()}
        return render(request, "orders/menu.html", context)
    context = {"status": "not logged in"}
    return render(request, "orders/index.html", context)


# just pass request. get form data with request.POST["input name"]
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
