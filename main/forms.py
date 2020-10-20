from django import forms
from .models import Photo, Category


class CatImageForm(forms.ModelForm):
    # """Form for the category image model"""
    class Meta:
        model = Category
        fields = ('name', 'cat_photo')

class ProductImageForm(forms.ModelForm):
    # """Form for the product model"""
    class Meta:
        model = Product
        fields = ('name', 'desc', 'quantity_purchased', 'quantity_sold', 'unit_price', 'category', 'photos', 'included_in_orders')

class PhotoImageForm(forms.ModelForm):
    # """Form for the photo model"""
    class Meta:
        model = Photo
        fields = ('img', 'type_of_photo', 'for_product' )