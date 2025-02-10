from django.shortcuts import render , redirect
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required # login required for functions
from django.contrib.auth.mixins import LoginRequiredMixin # login required for class based views
from django.shortcuts import get_object_or_404

import datetime

from .models import Order , CartDetails , Cart
from products.models import Product
from settings.models import DeliveryFee

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

def remove_from_checkout(request,id):
    cart_detail = CartDetails.objects.get(id=id)
    cart_detail.delete()
    return redirect('/orders/checkout')


@login_required 
def checkout(request):
    cart = Cart.objects.get(user=request.user,status='InProgress')
    cart_detail = CartDetails.objects.filter(cart=cart)
    delivery_fee = DeliveryFee.objects.last().fee

    if request.method == 'POST':
        coupon = get_object_or_404(Coupon,code=request.POST['coupon_code']) # 404 with out coupon
        # coupon = Coupon.objects.get(code=request.data['coupon_code']) # erorr without coupon


        if coupon and coupon.quantity > 0:
            today_date = datetime.datetime.today().date()

            if today_date >= coupon.start_date and coupon.end_date:
                coupon_value = cart.cart_total() * coupon.discount/100
                cart_total = cart.cart_total() - coupon_value

                coupon.quantity -= 1
                coupon.save()

                cart.coupon = coupon
                cart.total_after_coupon = cart_total
                cart.save()

                total = delivery_fee + cart_total

                cart = Cart.objects.get(user=request.user,status='InProgress')

                return render(request, 'orders/checkout.html',{
                    'cart_detail': cart_detail,
                    'cart_sub_total': cart_total,
                    'cart_total': total,
                    'coupon': coupon_value,
                })
                
    return render(request, 'orders/checkout.html',{'cart_detail':cart_detail})