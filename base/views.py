from django.shortcuts import render,redirect
from django.http import JsonResponse
import json
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import Customer, Product, Order, OrderItem, ShippingAddress,User
from django.contrib.auth.decorators import login_required

@login_required(login_url='signin')
def store(request):
    if request.user.is_authenticated:
        user = request.user.customer
        order, created = Order.objects.get_or_create(customer=user, complete=False)
        items = Product.objects.all()
        cart_items = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total': 0, "get_cart_items": 0}
        cart_items = order['get_cart_items']
    context = {"items": items, "order": order,'cart_items':cart_items}
    return render(request, 'base/store.html',context)

def updateItem(request):
    data = json.loads(request.body)
    product_id = data['p_Id']
    action = data['action']
    print(action)
    print(product_id)

    customer = request.user.customer
    product = Product.objects.get(id=product_id)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    orderitem, create = OrderItem.objects.get_or_create(order = order,product=product)
    
    if action == 'add':#add or remove items in the order
        orderitem.quantity = (orderitem.quantity + 1)
    elif action == 'remove':
        orderitem.quantity = (orderitem.quantity - 1)
    
    orderitem.save()

    if orderitem.quantity <= 0:#if there's no items the delete the order
        orderitem.delete()

    return JsonResponse('Item added', safe=False)
      
def cart(request):  # check if user is lgged in or not
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cart_items = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total': 0, "get_cart_items": 0}
        cart_items = order['get_cart_items']
    context = {"items": items, "order": order, 'cart_items': cart_items}
    
    return render(request, 'base/cart.html',context)


def checkout(request):#summary of the cart
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(
            customer=customer, complete=False)
        items = order.orderitem_set.all()
        cart_items = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total': 0, "get_cart_items": 0}
        cart_items = order['get_cart_items']
    context = {"items": items, "order": order, 'cart_items': cart_items}
    return render(request, 'base/checkout.html',context)

def shipping(request):
    context = {}
    return render(request, 'base/item_profile.html',context)

def itemProfile(request):
    context = {}
    return render(request, 'base/item_profile.html',context)


def signin(request):
    
    if request.method == "POST":
        email = request.POST.get("email")
        pass1 = request.POST.get("password")
        
        user = User.objects.get(email=email).username
        u = authenticate(username=user, password=pass1)

        if u is not None:
            login(request, u)
            return redirect("store")
        else:
            messages.error(request, 'Password is Incorrect')
            return redirect("signin")
      
    return render(request, 'base/signin.html')


def register(request):
    context = {}
    return render(request, 'base/register.html', context)


def signout(request):
    logout(request)
    return redirect('signin')
