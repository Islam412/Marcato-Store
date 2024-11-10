from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from django.db.models.aggregates import Avg

from taggit.managers import TaggableManager

from userauths.models import User

# Create your models here.


FLAG_TYPES=[
    ('Sale','Sale'),
    ('New','New'),
    ('Feature','Feature'),
]

class Product(models.Model):
    name = models.CharField(_('Name'),max_length=120)
    flag = models.CharField(_('Flag'),max_length=10,choices=FLAG_TYPES)
    image = models.ImageField(_('Image'),upload_to='products')
    price = models.FloatField(_('Price'))
    sku = models.CharField(_('SKU'),max_length=12)
    subtitle = models.CharField(_('Subtitle'),max_length=300)
    descripition = models.TextField(_('Descripition'),max_length=40000)
    quantity = models.IntegerField(_('Quantity'))
    brand = models.ForeignKey('Brand',verbose_name=_('Brand'), related_name='product_name', on_delete=models.SET_NULL, null = True)
    tags = TaggableManager()
    slug = models.SlugField(unique=True,null=True,blank=True)
    
    def __str__(self):
        return self.name
    
    # instance methods = each object , self=object
    def avg_rate(self):
        avg = self.review_product.aggregate(rate_avg=Avg('rate'))
        if not avg['rate_avg']:
            return 0
            return result
        return avg['rate_avg']
    
    def save(self, *args, **kwargs):
       self.slug = slugify(self.name)
       super(Product, self).save(*args, **kwargs)
       
    @property
    def average_rating(self):
        reviews = self.review_product.all()
        if reviews.count() > 0:
            total_rating = sum(review.rate for review in reviews)
            return total_rating / reviews.count()
        return 0  
    