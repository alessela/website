from django.contrib import admin

from .models import *
admin.site.register(Product)
admin.site.register(CartProduct)
admin.site.register(Order)
admin.site.register(OrderProduct)
admin.site.register(BankAccount)
