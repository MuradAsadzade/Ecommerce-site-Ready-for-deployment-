from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.


class WishItem(models.Model):
    product = models.ForeignKey('shop.Products', on_delete=models.CASCADE)
    customer = models.ForeignKey('Customer', on_delete=models.CASCADE, related_name='wishlist')
    created = models.DateTimeField(auto_now_add=True)

class BasketItem(models.Model):
    product = models.ForeignKey('shop.Products', on_delete=models.CASCADE)
    customer = models.ForeignKey('Customer', on_delete=models.CASCADE, related_name='basketlist')
    count = models.IntegerField(default=0)
    size = models.ForeignKey('shop.Size', on_delete=models.CASCADE)
    color = models.ForeignKey('shop.Color', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='customer')

    def __str__(self):
        return self.user.username

class Review(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='reviews')
    product = models.ForeignKey('shop.Products', on_delete=models.CASCADE, related_name='reviews')
    comment = models.TextField()
    star_count = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    created = models.DateField(auto_now_add=True)


class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.name
    

