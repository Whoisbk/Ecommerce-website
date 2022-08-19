from django.urls import path
from . import views

urlpatterns = [

  path("", views.store, name="store"),
  path("signin/", views.signin, name="signin"),
  path("cart/", views.cart, name="cart"),
  path("itemProfile/", views.itemProfile, name="item_profile"),
  path("register/", views.register, name="register"),
  path("checkout/", views.checkout, name="checkout"),

]
