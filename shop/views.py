from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from .models import Campaign, Category, Products
from django.db.models import Count
from customer.models import Review

# Create your views here.


def product_list(request):
    products = Products.objects.all()
    return render(request, 'product-list.html', {
        'products': products
    })



def home(request):
    slide_campaigns = Campaign.objects.filter(is_slide=True)[:3]
    nonslide_campaigns = Campaign.objects.filter(is_slide=False)[:4]
    categories = Category.objects.annotate(product_count=Count('products'))
    featured_products = Products.objects.filter(featured=True)[:8]
    recent_products = Products.objects.all().order_by('-created')[:8]

    return render(request, 'home.html', {
        'slide_campaigns': slide_campaigns,
        'nonslide_campaigns': nonslide_campaigns,
        'categories': categories,
        'featured_products': featured_products,
        'recent_products': recent_products,
    })


def product_detail(request, pk):
    product = get_object_or_404(Products, pk=pk)
    # other_products = Products.objects.filter(categories__in=product.categories.all()).annotate(common_product_count=Count('pk')).exclude(pk=product.pk).order_by('-common_product_count')
    other_products = Products.objects.exclude(pk=product.pk).order_by('?')[:5]

    user_review = request.user.is_authenticated and Review.objects.filter(customer=request.user.customer, product=product).first()
    # reviews = product.reviews.exclude(customer=user_review and user_review.customer)
    reviews = product.reviews.exclude(customer=request.user.is_authenticated and request.user.customer)
    return render(request, 'product-detail.html', {
        'product': product,
        'other_products': other_products,
        'user_review': user_review,
        'reviews': reviews,
    })

def review(request, pk):
    if request.method == 'POST':
        customer = request.user.customer
        product = get_object_or_404(Products, pk=pk)
        if Review.objects.filter(customer=customer, product=product).exists():
            return HttpResponse(status=403)
        star_count = int(request.POST.get('star_count'))
        comment = request.POST.get('comment')
        review = Review.objects.create(
            customer=customer, product=product,
            comment=comment, star_count=star_count
        )
        return redirect('shop:product-detail', pk=pk)
    return redirect('shop:home')