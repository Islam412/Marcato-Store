from django.shortcuts import render
from django.views.generic import ListView

from .models import Order

# Create your views here.

class OrderListView(ListView):
    model = Order
    ordering = ['-id']
    paginate_by = 10
    
    def get_queryset(self):
        queryset = super().get_queryset().filter(user=self.request.user)
        return queryset

