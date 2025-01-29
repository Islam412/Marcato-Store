from django.shortcuts import get_object_or_404

from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import generics
from rest_framework.response import Response

from .serializers import CartDetailSerializer , CartSerializer
from .models import Cart , CartDetails , Order, OrderDetails
from products.models import Product
from userauths.models import User




class CartDetailCreateAPI(generics.GenericAPIView):
    serializer_class = CartSerializer
    permission_classes = [AllowAny]

    def get(self,request,*args,**kwargs):
        user = User.objects.get(username=self.kwargs['username'])
        cart,created = Cart.objects.get_or_create(user=user,status='InProgress')
        data = CartSerializer(cart).data
        return Response({'cart':data})


    def post(self, request, *args, **kwargs):
        user = User.objects.get(username=self.kwargs['username'])
        product = Product.objects.get(id=request.data['product_id'])
        quantity = int(request.data['quantity'])
        cart = Cart.objects.get(user=user,status='InProgress')
        cart_detail , creeate = CartDetails.objects.get_or_create(cart=cart, product=product)
        cart_detail.quantity = int(quantity)
        cart_detail.total = round(quantity * product.price , 2)
        cart_detail.save()


        cart = Cart.objects.get(user=user,status='InProgress')
        data = CartSerializer(cart).data
        return Response({'message':'Cart item added successfully' ,'cart':data})

    def delete(self, request, *args, **kwargs):
        user = User.objects.get(username=self.kwargs['username'])
        cart_detail =CartDetails.objects.get(id=request.data['cart_detail_id'])
        cart_detail.delete()

        cart = Cart.objects.get(user=user,status='InProgress')
        data = CartSerializer(cart).data
        return Response({'message':'Cart item deleted successfully' ,'cart':data})