from django.shortcuts import redirect, render
from django.http import HttpResponse
from .models import *
import json
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib import messages
from .forms import CreateUserForm



# Create your views here.
def register(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
    context= {'form': form}
    return render(request, 'app/register.html', context)
def loginPage(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('home')
        else: 
            messages.error(request, 'Tên đăng nhập hoặc mật khẩu không đúng!')
    context= {}
    return render(request, 'app/login.html', context)
def home(request):
    products = Product.objects.all()
    context= {'products': products}
    return render(request, 'app/home.html', context)
def base(request):
    context= {}
    return render(request, 'app/base.html', context)
def cart(request):
    if request.user.is_authenticated:
        customer, created = Customer.objects.get_or_create(user=request.user)
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {'total_amount':0, 'total_items':0}
    context= {'items': items, 'order': order}
    return render(request, 'app/cart.html', context)
def checkout(request):
    if request.user.is_authenticated:
        customer, created = Customer.objects.get_or_create(user=request.user)
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {'total_amount':0, 'total_items':0}
    context = {'items': items, 'order': order}
    return render(request, 'app/checkout.html', context)
