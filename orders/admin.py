from django.contrib import admin
from .models import Cart,CartDetails,Order,OrderDetails,Coupon,DeliveryAddress,DeliveryPhone,CreditCard ,Delivery

# Register your models here.

class DeliveryAdmin(admin.ModelAdmin):
    list_display = ['user','address' , 'phone']
    search_fields = ['user__username', 'phone', 'address']
    ordering = ['user']



admin.site.register(Cart)
admin.site.register(CartDetails)
admin.site.register(Order)
admin.site.register(OrderDetails)
admin.site.register(Coupon)
admin.site.register(DeliveryAddress)
admin.site.register(DeliveryPhone)
admin.site.register(CreditCard)
admin.site.register(Delivery,DeliveryAdmin)
