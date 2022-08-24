from django.shortcuts import render,redirect
from django.http import JsonResponse
import json
from datetime import datetime
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import Customer, Product, Order, OrderItem, ShippingAddress,User
from django.contrib.auth.decorators import login_required
import time
from .filters import *


def store(request):
    if request.user.is_authenticated:
        user = request.user.customer
        order, created = Order.objects.get_or_create(customer=user, complete=False)
        items = Product.objects.all()
        cart_items = order.get_cart_items

        store_filter = StoreFilter(request.GET, queryset=items)
        items = store_filter.qs
    else:
        order = {'get_cart_total': 0, "get_cart_items": 0}
        cart_items = order['get_cart_items']
        items = Product.objects.all()
        
    context = {"items": items, "order": order,'cart_items':cart_items,'store_filter':store_filter}
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
       return redirect('signin')
        
    context = {"items": items, "order": order, 'cart_items': cart_items}
    
    return render(request, 'base/cart.html',context)


def checkout(request):  #summary of the cart
    
    customer = request.user.customer
    order, created = Order.objects.get_or_create(
        customer=customer, complete=False)
    items = order.orderitem_set.all()
    cart_items = order.get_cart_items

    if request.method == 'POST':
        address = request.POST.get('address')
        city = request.POST.get('city')
        country = request.POST.get('country')
        zip_code = request.POST.get('zip')
        shipped = True
        shipping_address = ShippingAddress(customer= customer,order=order,address = address,city = city,state = country,zipcode=zip_code )
        shipping_address.save()
        return redirect('payment') 

    context = {"items": items, "order": order, 'cart_items': cart_items,'customer':customer}
    return render(request, 'base/checkout.html',context)


def payment(request):
    transaction_id = datetime.now().timestamp()

    if request.user.is_authenticated:  
        customer = request.user.customer
        order, created = Order.objects.get_or_create(
            customer=customer, complete=False)
        items = order.orderitem_set.all()
        cart_items = order.get_cart_items
        order.transaction_id = transaction_id
        order.complete = True
        order.save()
    else:
        return redirect('signin')

    context = {"items": items, "order": order, 'cart_items': cart_items}
    return render(request, 'base/payment.html',context)

def itemProfile(request,pk):
    context = {}

    item = Product.objects.get(name=pk)
    
    context = {"item":item}
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
