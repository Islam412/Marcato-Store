from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny

from .serializers import ProductSerializers , BrandListSerializers , BrandDetailSerializers
from .models import Product , Brand


# Functions api
@api_view(['GET'])
def product_list_api(request):
    products = Product.objects.all()[:20]
    data = ProductSerializers(products, many=True , context={'request':request}).data
    return Response({'products':data})



@api_view(['GET','POST'])  # GET Show all data | POST Update data
def product_detail_api(request,product_name):
    products = Product.objects.get(id=product_name)
    data = ProductSerializers(products, context={'request':request}).data
    return Response({'products':data})


# class generic view api
class ProductListAPI(generics.ListCreateAPIView):  # list show all dsta | create update data
    queryset = Product.objects.all()
    serializer_class = ProductSerializers
    permission_classes = [AllowAny]


class ProductDetailAPI(generics.RetrieveUpdateDestroyAPIView): 
    queryset = Product.objects.all()
    serializer_class = ProductSerializers
    permission_classes = [AllowAny]


class BrandListAPI(generics.ListCreateAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrandListSerializers
    permission_classes = [AllowAny]


class BrandDetailAPI(generics.RetrieveUpdateDestroyAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrandDetailSerializers
    permission_classes = [AllowAny]