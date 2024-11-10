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
    


class ProductDetails(DetailView):
    model = Product
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.get_object()
        context["reviews"] = Review.objects.filter(product=product)
        context["average_rating"] = product.average_rating
        context["rate_products"] = Product.objects.filter(brand=product.brand)
        return context
    


class BrandList(ListView):
    model = Brand
    queryset = Brand.objects.annotate(products_count=Count('product_name'))
    paginate_by = 20


class BrandDetails(ListView):
    model = Product
    paginate_by = 20
    template_name = 'products/brand_detail.html'
    
    def get_queryset(self):
        brand = Brand.objects.get(slug=self.kwargs['slug'])
        return super().get_queryset().filter(brand=brand)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        brand = Brand.objects.annotate(products_count=Count('product_name')).get(slug=self.kwargs['slug'])
        context["brand"] = brand  

        return context 