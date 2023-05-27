from django.db import models
from django.utils import timezone


# Create your models here.

class Coupon(models.Model):
    title = models.CharField(max_length=50)
    code = models.CharField(max_length=20)
    discount = models.FloatField()
    used_customers = models.ManyToManyField('customer.Customer', related_name='used_coupons', blank=True)  
    expire = models.DateTimeField()
    limit = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
    def is_valid(self, customer):
        if timezone.localtime() > self.expire:
            return [False, 'Bu kuponun tarixi kecmisdir']
        elif self.used_customers.count() >= self.limit:
            return [False, 'Bu kuponun limiti bitmisdir']
        elif self.used_customers.contains(customer):
            return [False, 'Siz artiq bu kupondan istifade etmisiniz']
        else:
            return [True, 'Kupon ugurla istifade olundu']



COUNTRIES = [
    ('azerbaijan', 'Azerbaijan'),
    ('turkey', 'Turkey'),
    ('russia', 'Russia'),
    ('usa', 'USA'),
    ('uk', 'UK'),
    ('germany', 'Germany'),
    ('france', 'France'),
]

class Order(models.Model):
    customer = models.ForeignKey('customer.Customer', on_delete=models.SET_NULL, null=True)
    coupon_code = models.CharField(max_length=20, blank=True, null=True)    
    coupon_discount = models.IntegerField(default=0)
    accepted = models.BooleanField(default=False)
    delivered = models.BooleanField(default=False)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    mobile = models.CharField(max_length=50)
    country = models.CharField(max_length=50, choices=COUNTRIES)
    city = models.CharField(max_length=50)
    address = models.CharField(max_length=50)
    zip_code = models.CharField(max_length=50)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.first_name + ' ' + self.last_name

class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='products')
    title = models.CharField(max_length=50)
    count = models.IntegerField(default=1)
    price = models.FloatField()
    size = models.CharField(max_length=50)
    color = models.CharField(max_length=50)
    created = models.DateTimeField(auto_now_add=True) 