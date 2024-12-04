from django.contrib import admin
from .models import *

# Register your models here.


admin.site.register(Product)
admin.site.register(Bill)
admin.site.register(Customer)
admin.site.register(BillItem)
admin.site.register(BillItemProduct)