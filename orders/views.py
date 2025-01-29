from django.shortcuts import render , redirect
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required # login required for functions
from django.contrib.auth.mixins import LoginRequiredMixin # login required for class based views


from .models import Order , CartDetails , Cart
from products.models import Product

# Create your views here.

class OrderListView(LoginRequiredMixin , ListView):
    model = Order
    ordering = ['-id']
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset().filter(user=self.request.user)
        return queryset
    

def add_to_cart(request):
    quantity = request.POST['quantity']
    product = Product.objects.get(id=request.POST['product_id'])

    cart = Cart.objects.get(user = request.user, status='InProgress')
    cart_detail , creeate = CartDetails.objects.get_or_create(cart=cart, product=product)

    cart_detail.quantity = int(quantity)
    cart_detail.total = round(int(quantity) * product.price , 2)
    cart_detail.save()

    return redirect (f'/products/{product.slug}')


def remove_from_cart(request,id):
    cart_detail = CartDetails.objects.get(id=id)
    cart_detail.delete()
    return redirect('/products/')


@login_required 
def checkout(request):
    cart = Cart.objects.get(user=request.user,status='InProgress')
    cart_detail = CartDetails.objects.filter(cart=cart)
    return render(request, 'orders/checkout.html',{'cart_detail':cart_detail})