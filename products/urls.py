from django.urls import path
from .views import ProductDetails, ProductList, BrandList, BrandDetails, queryset_debug , product_search , product_filter , product_filter_by_flag

app_name = 'products'

urlpatterns = [
    path('brands/', BrandList.as_view(), name='brand_list'),
    path('search/', product_search, name='product_search'),
    path('filter/', product_filter, name='product_filter'),
    path('filter-by-tags/', product_filter_by_flag, name='product_filter_by_tags'),
    path('', ProductList.as_view(), name='product_list'),
    path('debug/', queryset_debug, name='queryset_debug'),  # Debugging tool for testing queryset performance.
    path('<slug:slug>/', ProductDetails.as_view(), name='product_detail'),
    path('brands/<slug:slug>/', BrandDetails.as_view(), name='brand_detail'),
]