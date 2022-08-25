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


@login_required(login_url='signin')
def store(request):
    
    user = request.user.customer
    order, created = Order.objects.get_or_create(customer=user, complete=False)
    items = Product.objects.all()
    cart_items = order.get_cart_items
    #search form
    store_filter = StoreFilter(request.GET, queryset=items)
    items = store_filter.qs
    
    context = {"items": items, "order": order,'cart_items':cart_items,'store_filter':store_filter}
    return render(request, 'base/store.html',context)


@login_required(login_url='signin')
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


@login_required(login_url='signin')
def cart(request):  # check if user is lgged in or not
    customer = request.user.customer
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    items = order.orderitem_set.all()
    cart_items = order.get_cart_items

    context = {"items": items, "order": order, 'cart_items': cart_items}
    
    return render(request, 'base/cart.html',context)


@login_required(login_url='signin')
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


@login_required(login_url='signin')
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
        try:
            if email == "":
                messages.error(request, 'Email is empty')
                return redirect("signin")
            elif not User.objects.filter(email=email):
                messages.error(request, 'Create an Account')
                return redirect("signin")
            elif pass1 == "":
                messages.error(request, 'Please enter password')
                return redirect("signin")

            user = User.objects.get(email=email).username
            u = authenticate(username=user, password=pass1)
        except  Exception as e:
            messages.error(request,'Email is incorrect')
            return redirect("signin")
    
        if u is not None:
            login(request, u)
            return redirect("store")
        else:
            messages.error(request, 'Password is Incorrect')
            return redirect("signin")
      
    return render(request, 'base/signin.html')


def register(request):
    
    if request.method == "POST":
        email = request.POST.get('email')
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        un = request.POST.get('username')
        p1 = request.POST.get('pass-1')
        p2 = request.POST.get('pass-2')
        special_Sym = ["@", "!", "$", "#"]

        if p1 != p2:  # if passwords are not equal
            messages.error(request, "Passwords are not equal")
        elif fname == "":
            messages.error(request, "Enter your name")
        elif lname == "":
            messages.error(request, "Enter your last name")
        elif len(p1) < 6:  # if password is too short
            messages.error(
                request, "Password is too short must be more than 6 characters")
        # if password does'nt have any special character
        elif not any(char in special_Sym for char in p1):
            messages.error(
                request, "Password must have a special Character @!$#")
        elif User.objects.filter(email=email):  # if email already exists
            messages.error(request, "Email already exists")
    
        elif email == '':#if email is empty
            messages.error(request, "Please enter you email")
        # if username already exists
        elif User.objects.filter(username=un):
            messages.error(request, "Username already exists")
            
        elif un == "":  # if username is empty
            messages.error(request, "Username is empty")
            
        elif len(un) < 4:  # if username is too short
            messages.error(
                request, "Username is too short must be more than 4 characters")
            
        else:
            u = User.objects.create_user(un, email, p1)
            u.first_name = fname
            u.last_name = lname

            customer = Customer(user=u, name=fname, email=email)
            customer.save()

            return redirect('signout')

    return render(request, 'base/register.html')


def signout(request):
    logout(request)
    messages.success(request, "logged out")
    return redirect('signin')
