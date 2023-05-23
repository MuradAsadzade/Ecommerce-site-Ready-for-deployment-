from django.shortcuts import render, redirect, get_object_or_404
from .forms import ContactForm, RegisterForm
from shop.models import Products
from .models import WishItem, BasketItem
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, F

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
    total_price = wishlist.aggregate(total_price = Sum('product__price'))['total_price']
    # Author.objects.annotate(total_pages=Sum("book__pages"))
    return render(request, 'wishlist.html', {'wishlist': wishlist, 'total_price': total_price,})

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

@login_required
def basket(request):
    basketlist = request.user.customer.basketlist.all().annotate(total_price=F('count') * F('product__price'))
    all_price = basketlist.aggregate(all_price=Sum('total_price'))['all_price']
    shipping_price = all_price * 0.07
    final_price = all_price + shipping_price
    return render(request, 'basket.html', {
        'basketlist' : basketlist,
        'all_price' : all_price,
        'shipping_price' : shipping_price,
        'final_price' : final_price,
    })

@login_required
def add_basket(request, product_pk):
    if request.method == 'POST':
        size_pk = request.POST.get('size')
        color_pk = request.POST.get('color')
        count = request.POST.get('count')
        customer = request.user.customer
        basket = BasketItem.objects.create(product_id=product_pk, size_id=size_pk, color_id=color_pk, count=count, customer=customer)
        return redirect(request.META.get('HTTP_REFERER'))
    else:
        return redirect('shop:home')
    
@login_required
def increase_basket_item(request, basket_pk):
    basket = get_object_or_404(BasketItem, pk=basket_pk)
    basket.count = F('count') + 1
    basket.save()
    return redirect('customer:basket')

@login_required
def decrease_basket_item(request, basket_pk):
    basket = get_object_or_404(BasketItem, pk=basket_pk)
    if basket.count == 1:
        basket.delete()
    else:
        basket.count = F('count') - 1
        basket.save()
    return redirect('customer:basket')

@login_required
def remove_basket(request, basket_pk):
    basket = get_object_or_404(BasketItem, pk=basket_pk)
    basket.delete()
    return redirect('customer:basket')

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


