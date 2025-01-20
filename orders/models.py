from django.db import models
from django.utils import timezone

from userauths.models import User
from products.models import Product
# Create your models here.


CART_STATUS = [
    ('InProgress','InProgress'),
    ('Completed','Completed'),
]

class Cart(models.Model):
    user = models.ForeignKey(User,related_name='cart_user', on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=10,choices=CART_STATUS)


class CartDetails(models.Model):
    cart = models.ForeignKey(Cart,related_name='cart_details', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='cart_product', on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.IntegerField()
    total = models.FloatField(null=True,blank=True)


ORDER_STATUS = [
    ('Recieved','Recieved'),
    ('Processed','Processed'),
    ('Shipped','Shipped'),
    ('Delivered','Delivered'),
]

class Order(models.Model):
    user = models.ForeignKey(User,related_name='order_user', on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=10,choices=ORDER_STATUS)
    code = models.CharField()
    order_time = models.DateTimeField(default=timezone.now())
    delivery_time = models.DateTimeField(null=True, blank=True)

class OrderDetails(models.Model):
    order = models.ForeignKey(Order,related_name='order_details', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='order_product', on_delete=models.SET_NULL, null=True, blank=True)
    price = models.FloatField()
    quantity = models.IntegerField()
    total = models.FloatField(null=True,blank=True)


class Coupon(models.Model):
    code = models.CharField(max_length=20)