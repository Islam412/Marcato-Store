from django.urls import path

from .views import OrderListView, checkout , add_to_cart , remove_from_cart



app_name = 'orders'

urlpatterns = [
    path('', OrderListView.as_view(), name='order_list'),
    path('checkout/', checkout, name='checkout'),
    path('add-to-cart/', add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<int:id>', remove_from_cart, name='remove_from_cart'),
]
