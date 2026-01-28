from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Store)
admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Inventory)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Payment)
admin.site.register(StockTransaction)