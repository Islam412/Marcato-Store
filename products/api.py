from rest_framework.decorators import api_view
from rest_framework.response import Response

from .serializers import ProductSerializers
from .models import Product


@api_view(['GET'])
def product_list_api(request):
    products = Product.objects.all()[:20]
    data = ProductSerializers(products, many=True , context={'request':request}).data
    return Response({'products':data})



@api_view(['GET'])
def product_detail_api(request,product_name):
    products = Product.objects.get(id=product_name)
    data = ProductSerializers(products, context={'request':request}).data
    return Response({'products':data})