from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.ulogin, name="login"),
    path("logout", views.ulogout, name="logout"),
    path("register", views.uregister, name="register")
]
