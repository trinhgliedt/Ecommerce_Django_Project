from django.urls import path

from . import views
from .views import SearchResultsView

urlpatterns = [
    path('', views.index),
    path('product/category/<int:cat_id>', views.display_category),
    path('product/category/<int:cat_id>/item/<int:product_id>', views.display_product),
    path('add_to_cart', views.add_to_cart),
    path('success', views.display_success),
    path('shopping_cart', views.display_shopping_cart),
    path('shopping_cart/process', views.process_shopping_cart),

    path('search/', SearchResultsView.as_view(), name='search_results'),
    

    path('product/category/<int:cat_id>/item/<int:product_id>/<int:photo_id>', views.switch_main_image),
    path('restore_stock', views.restore_stock),


    
]