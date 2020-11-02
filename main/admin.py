from django.contrib import admin
from .models import Photo, Category, Product, Order
# Register your models here.
admin.site.register(Photo)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Order)