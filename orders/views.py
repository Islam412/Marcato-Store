from django.shortcuts import render
from django.views.generic import ListView

from .models import Order , CartDetails

# Create your views here.

class OrderListView(ListView):
    model = Order
    ordering = ['-id']
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset().filter(user=self.request.user)
        return queryset


def checkout(request):
    cart = Order.objects.get(user=request.user,status='InProgress')
    cart_detail = CartDetails.objects.filter(cart=cart)
    return render(request, 'orders/checkout.html',{'cart_detail':cart_detail})