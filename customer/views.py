from django.shortcuts import render, redirect, get_object_or_404
from .forms import ContactForm, RegisterForm
from shop.models import Products
from .models import WishItem
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required

# Create your views here.


def contact(request):
    form = ContactForm()
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'contact.html', {'form': form, 'result': 'success'})
        return render(request, 'contact.html', {'form': form, 'result': 'fail'})
    return render(request, 'contact.html', {'form': form})

@login_required
def wishlist_view(request):
    wishlist = request.user.customer.wishlist.all()
    return render(request, 'wishlist.html', {'wishlist': wishlist,})

@login_required
def wish_products(request, pk):
    product = get_object_or_404(Products, pk=pk)
    customer = request.user.customer
    WishItem.objects.create(product=product, customer=customer)
    return redirect(request.META.get('HTTP_REFERER'))

@login_required
def unwish_products(request, pk):
    product = get_object_or_404(Products, pk=pk)
    customer = request.user.customer
    WishItem.objects.filter(product=product, customer=customer).delete()
    return redirect(request.META.get('HTTP_REFERER'))

def basket(request):
    return render(request, 'basket.html', {})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return redirect('shop:home')
        return render(request, 'login.html', {'fail': True})
    return render(request, 'login.html', {'fail': False})

def register(request):
    form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            print('duzdu')
            customer = form.save()
            login(request, customer.user)
            return redirect('shop:home')
        print('salam')
    return render(request, 'register.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('customer:login')