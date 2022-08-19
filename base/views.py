from django.shortcuts import render
from .models import Customer, Product, Order, OrderItem, ShippingAddress

def store(request):
    items = Product.objects.all()
    context = {"items":items}
    
    return render(request, 'base/store.html',context)
    
def cart(request):  # check if user is lgged in or not
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {'get_cart_total': 0,"get_cart_items": 0}
    context = {"items":items,"order":order}
    return render(request, 'base/cart.html',context)


def checkout(request):#summary of the cart
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(
            customer=customer, complete=False)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {'get_cart_total': 0, "get_cart_items": 0}
    context = {"items": items, "order": order}
    context = {}
    return render(request, 'base/checkout.html',context)

def shipping(request):
    context = {}
    return render(request, 'base/item_profile.html',context)

def itemProfile(request):
    context = {}
    return render(request, 'base/item_profile.html',context)


def signin(request):
    context = {}
    return render(request, 'base/login.html',context)


def register(request):
    context = {}
    return render(request, 'base/register.html',context)
