from django.shortcuts import render
from .models import Customer, Product, Order, OrderItem, ShippingAddress

# Create your views here.

def store(request):
    items = Product.objects.all()
    context = {"items":items}

    return render(request, 'base/store.html',context)
    
def cart(request):
    context = {}
    return render(request, 'base/cart.html',context)


def checkout(request):
    context = {}
    return render(request, 'base/checkout.html',context)


def itemProfile(request):
    context = {}
    return render(request, 'base/item_profile.html',context)


def signin(request):
    context = {}
    return render(request, 'base/login.html',context)


def register(request):
    context = {}
    return render(request, 'base/register.html',context)
