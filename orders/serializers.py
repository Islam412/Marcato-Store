from rest_framework import serializers

from .models import Cart , CartDetails , Order , OrderDetails
from products.serializers import ProductListSerializers


class CartDetailSerializer(serializers.Serializer):
    # product = ProductListSerializers()
    product = serializers.StringRelatedField()
    class Meta:
        model = CartDetails
        fields = '__all__'


class CartSerializer(serializers.ModelSerializer):
    cart_details = CartDetailSerializer(many=True)

    class Meta:
        model = Cart
        fields = '__all__'