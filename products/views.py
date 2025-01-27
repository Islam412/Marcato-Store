from django.shortcuts import render
from django.views.generic import ListView , DetailView
from django.db.models import Q , F , Value , Count
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
    ordering = ['-id']



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
    ordering = ['-id']



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
    


# search and filter with category
def product_search(request):
    query = request.GET.get('q', '')
    if query:
        # Search products by name, description, or SKU
        products = Product.objects.filter(
            Q(name__icontains=query) | 
            Q(descripition__icontains=query) |
            Q(sku__icontains=query) |
            Q(tags__name__icontains=query)
        ).distinct()
    else:
        products = Product.objects.all()
    
    return render(request, 'products/product_search.html', {'product_list': products})


def product_filter(request):
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')

    products = Product.objects.all()
    if min_price:
        products = products.filter(price__gte=float(min_price))
    if max_price:
        products = products.filter(price__lte=float(max_price))
    
    return render(request, 'products/product_filter.html', {'products': products})


def product_filter_by_flag(request):
    tags = request.GET.getlist('tags')
    products = Product.objects.all()

    if tags:
        products = products.filter(flag__in=tags)

    return render(request, 'products/product_filter.html', {'products': products})

