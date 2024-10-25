from django.contrib import admin
from .models import Ad, Order, Transaction, Category


admin.site.register(Ad)
admin.site.register(Category)
admin.site.register(Transaction)
admin.site.register(Order)
