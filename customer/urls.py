from django.urls import path
from . import views

app_name = 'customer'

urlpatterns = [
    path('contact/', views.contact, name='contact'),
    path('wishlist/', views.wishlist_view, name='wishlist'),
    path('basket/', views.basket, name='basket'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('wish-product/<int:pk>', views.wish_products, name='wish-product'),
    path('unwish-product/<int:pk>', views.unwish_products, name='unwish-product'),
]
