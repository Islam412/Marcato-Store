from django.shortcuts import render
from django.views.generic import ListView , DetailView
from django.db.models import Q , F , Value
from django.db.models.aggregates import Max,Min,Count,Avg,Sum


from .models import Product, Brand, ProductImage, Review




def queryset_debug(request):
    
    # data = Product.objects.all()
    
    # data = Product.objects.filter(price__gt=80, quantity__lt=10)  #and
    
    # data = Product.objects.filter(Q(price__gt=80) & Q(quantity__lt=10))  #or
    
    data = Product.objects.annotate(price_with_tax=F('price')*1.2) # add new tower
    
    return render(request, 'products/queryset_debug.html', {'data': data})


class ProductList(ListView):
    model = Product
    paginate_by = 30
    