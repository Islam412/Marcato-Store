from django.shortcuts import render
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required # login required for functions
from django.contrib.auth.mixins import LoginRequiredMixin # login required for class based views


from .models import Order , CartDetails , Cart

# Create your views here.

class OrderListView(LoginRequiredMixin , ListView):
    model = Order
    ordering = ['-id']
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset().filter(user=self.request.user)
        return queryset


@login_required 
def checkout(request):
    cart = Cart.objects.get(user=request.user,status='InProgress')
    cart_detail = CartDetails.objects.filter(cart=cart)
    return render(request, 'orders/checkout.html',{'cart_detail':cart_detail})