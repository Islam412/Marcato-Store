from django.db.models.aggregates import Avg
from rest_framework import serializers


from .models import Product , Brand


class ProductListSerializers(serializers.ModelSerializer):
    avg_rate = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = '__all__'

    def get_avg_rate(self, product):
        avg = product.review_product.aggregate(rate_avg=Avg('rate'))
        if not avg['rate_avg']:
            return 0
        return avg['rate_avg']



class ProductDetailSerializers(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class BrandListSerializers(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = '__all__'


class BrandDetailSerializers(serializers.ModelSerializer):
    products = ProductListSerializers(source='product_name', many=True)
    class Meta:
        model = Brand
        fields = '__all__'