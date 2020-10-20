from django.contrib import admin
from .models import Photo, Category, Product
# Register your models here.
admin.site.register(Photo)
admin.site.register(Category)
admin.site.register(Product)