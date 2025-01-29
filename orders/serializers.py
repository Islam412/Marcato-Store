from rest_framework import serializers

from .models import Cart , CartDetails , Order , OrderDetails


class CartDetailSerializer(serializers.Serializer):
    class Meta:
        model = CartDetails
        fields = '__all__'


