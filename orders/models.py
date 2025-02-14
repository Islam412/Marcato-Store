from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


from userauths.models import User
from products.models import Product

import datetime
import random
# Create your models here.


CART_STATUS = [
    ('InProgress','InProgress'),
    ('Completed','Completed'),
]

class Cart(models.Model):
    user = models.ForeignKey(User,related_name='cart_user', on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(_('Status'),max_length=10,choices=CART_STATUS)
    coupon = models.ForeignKey('Coupon',related_name='cart_coupon', on_delete=models.SET_NULL, blank=True , null=True)
    total_after_coupon = models.FloatField(_('Total After Coupon'),null=True,blank=True)


    def __str__(self):
        return str(self.user)
    
    def cart_total(self):
        total = 0
        for item in self.cart_details.all():
            total += item.total
        return round(total,2)
    


class CartDetails(models.Model):
    cart = models.ForeignKey(Cart,related_name='cart_details', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='cart_product', on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.IntegerField(_('Quantity'),default=1)
    total = models.FloatField(_('Total'),null=True,blank=True)

    def __str__(self):
        return str(self.cart)


def generate_code(length=10):
    data = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    code = ''.join(random.choice(data) for _ in range(length))
    return code

ORDER_STATUS = [
    ('Recieved','Recieved'),
    ('Processed','Processed'),
    ('Shipped','Shipped'),
    ('Delivered','Delivered'),
]
class Order(models.Model):
    user = models.ForeignKey(User,related_name='order_user', on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(('Status'), max_length=10,choices=ORDER_STATUS,default='Recieved')
    code = models.CharField(_('Code'), max_length=20,default=generate_code)
    order_time = models.DateTimeField(default=timezone.now)
    delivery_time = models.DateTimeField(_('Delivery Time'),null=True, blank=True)
    coupon = models.ForeignKey('Coupon',related_name='order_coupon', on_delete=models.SET_NULL, blank=True , null=True)
    total_after_coupon = models.FloatField(_('Total After Coupon'),null=True,blank=True)

    def __str__(self):
        return str(self.user)
    



class OrderDetails(models.Model):
    order = models.ForeignKey(Order,related_name='order_details', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='order_product', on_delete=models.SET_NULL, null=True, blank=True)
    price = models.FloatField(('Price'))
    quantity = models.IntegerField(_('Quantity'))
    total = models.FloatField(_('Total'), null=True,blank=True)

    def __str__(self):
        return str(self.order)


class Coupon(models.Model):
    image = models.ImageField(_('Image'),upload_to='coupon', blank=True, null=True)
    code = models.CharField(_('Code'), max_length=20)
    discount = models.IntegerField(_('Discount'))
    quantity = models.IntegerField(_('Quantity'))
    start_date = models.DateField(_('Start Date'), default=timezone.now)
    end_date = models.DateField(_('End Date'), null=True,blank=True)

    def __str__(self):
        return self.code
    

    def save(self, *args, **kwargs):
       week = datetime.timedelta(days=7)
       self.end_date = self.start_date + week
       super(Coupon, self).save(*args, **kwargs)  # call the real save method


class Delivery(models.Model):
    user = models.ForeignKey(User, related_name='delivery',on_delete=models.CASCADE)
    express = models.CharField(_('Express'),max_length=200, blank=True,null=True)
    start_work = models.DateTimeField(_('Start Work'),null=True,blank=True)
    end_work = models.DateTimeField(_('End Work'),null=True,blank=True)
    # address = models.ForeignKey('DeliveryAddress', related_name='delivery_address',on_delete=models.CASCADE)
    # phone = models.ForeignKey('DeliveryPhone', related_name='delivery_phoens',on_delete=models.CASCADE)


    def __str__(self):
        return f"{self.user}"


ADDRESS_TYPE = [
    ('Home', 'Home'),
    ('Work', 'Work'),
    ('Bussinees','Bussinees'),
    ('Office','Office'),
    ('Academy','Academy'),
    ('Other','Other'),
]

class DeliveryAddress(models.Model):
    user = models.ForeignKey(User,related_name='delivery_address',on_delete=models.CASCADE)
    type = models.CharField(_('Type'),max_length=20,choices=ADDRESS_TYPE)
    address = models.TextField(_('Address'),max_length=300)
    notes = models.TextField(_('Notes'),null=True,blank=True)

    def __str__(self):
        return f"{self.type} - {self.address}"


Phone_TYPE = [
    ('Primary','Primary'),
    ('Secondary','Secondary'),
    ('Third','Third')
]


class DeliveryPhone(models.Model):
    user = models.ForeignKey(User, related_name='delivery_phone', on_delete=models.CASCADE)
    type = models.CharField(_('Type'),max_length=20, choices=Phone_TYPE)
    phone = models.CharField(_('Notes'),max_length=30)

    def __str__(self):
        return f"{self.type} - {self.phone}"

class CreditCard(models.Model):
    user = models.ForeignKey(User, related_name='credit_cards', on_delete=models.CASCADE)
    image = models.ImageField(_('Image'), upload_to='Images_credit', null=True, blank=True, default='credit.webp')
    name = models.CharField(_('Name'),max_length=225)
    card_number = models.CharField(_('Card Number'),max_length=16)
    country = models.CharField(_('Country'),max_length=225)
    cvv = models.CharField(_('CVV'),max_length=3)
    expiration_date = models.DateField(_('Expiration Date'),)

    def __str__(self):
        return f"Card ending in {self.card_number[-4:]} - {self.user.username}"