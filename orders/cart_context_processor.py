from .models import Cart, CartDetails , DeliveryAddress

def get_or_create_cart(request):
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user, status='InProgress')
        if not created:
            cart_detail = CartDetails.objects.filter(cart=cart)  # Renamed cart_detail to cart_detail_data
            return {'cart_data': cart, 'cart_detail_data': cart_detail}  # Renamed cart_detail to cart_detail_data
        return {'cart_data': cart}
    else:
        return {}




# def get_delivery_address_data(request):
#     if request.user.is_authenticated:
#         delivery_address_data = DeliveryAddress.objects.filter(user=request.user)
#         return {'delivery_address_list': delivery_address_data}  # Changed key to "delivery_address_list"
#     return {'delivery_address_list': None}

