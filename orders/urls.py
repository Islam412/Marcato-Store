from django.urls import path

from .views import OrderListView, checkout



app_name = 'orders'

urlpatterns = [
    path('', OrderListView.as_view(), name='order_list'),
    path('checkout/', checkout, name='checkout'),
]
