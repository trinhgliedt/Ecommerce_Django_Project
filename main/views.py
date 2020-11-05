from django.shortcuts import render, redirect
from .models import *
import bcrypt
from django.contrib import messages
# from django.template.loader import render_to_string
# from django.http import JsonResponse
# from datetime import datetime
# from time import strftime, strptime
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# below: imports for search
from django.views.generic import ListView, TemplateView
from django.db.models import Q


def index(request):
    if "cart_dict" not in request.session:
        quantity_in_cart = 0
    else:
        quantity_in_cart = 0
        for key in request.session["cart_dict"]:
            quantity_in_cart += request.session["cart_dict"][key]
    # print('request.session["cart_dict"]: ', request.session["cart_dict"])
    context = {
        "all_categories": Category.objects.all(),
        "quantity_in_cart": quantity_in_cart,
    }
    return render(request, '_1_shop_main.html', context)

def display_category(request, cat_id ):

    product_list = Product.objects.filter(category_id=cat_id).exclude(temp_quan_avail=0)
    products_by_price = product_list.order_by("unit_price")
    page = request.GET.get('page', 1)
    paginator = Paginator(product_list, 8)
    try:
        all_products = paginator.page(page)
    except PageNotAnInteger:
        all_products = paginator.page(1)
    except EmptyPage:
        all_products = paginator.page(paginator.num_pages)
        
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    if "cart_dict" not in request.session:
        quantity_in_cart = 0
    else:
        quantity_in_cart = 0
        for key in request.session["cart_dict"]:
            quantity_in_cart += request.session["cart_dict"][key]
    # print('request.session["cart_dict"]: ', request.session["cart_dict"])

    context = {
        "all_categories": Category.objects.all(),
        "this_category": Category.objects.get(id=cat_id),
        "all_products": all_products,
        "products_by_price": products_by_price,
        "all_photos": Photo.objects.all(),
        "paginator": paginator,
        'page_obj': page_obj,
        "quantity_in_cart": quantity_in_cart,
    }

    return render(request, '_2_shop_category.html', context)

def display_product(request, cat_id, product_id ):
    price_1 = Product.objects.get(id=product_id).unit_price
    price_2 = Product.objects.get(id=product_id).unit_price*2
    price_3 = Product.objects.get(id=product_id).unit_price*3
    if "cart_dict" not in request.session:
        request.session["cart_dict"] ={};
        quantity_in_cart = 0
    else:
        quantity_in_cart = 0
        for key in request.session["cart_dict"]:
            quantity_in_cart += request.session["cart_dict"][key]

    context = {
        "this_product": Product.objects.get(id=product_id),
        "this_category": Category.objects.get(id=cat_id),
        "similar_items": Product.objects.filter(category_id=cat_id),
        "price_1": price_1,
        "price_2": price_2,
        "price_3": price_3,
        "product_class": Product,
        "quantity_in_cart": quantity_in_cart,
    }
    print('request.session["cart_dict"]: ', request.session["cart_dict"])
    print("quantity_in_cart: ", quantity_in_cart)
    print("request.POST: ", request.POST)
    return render(request, '_3_shop_prod_info.html', context)

def display_similar_product(request, this_category_id, product_id ):

    context = {
        "cat_id": this_category_id, 
        "product_id": product_id,
    }
    return redirect(f'product/category/<int:cat_id>/item/<int:product_id>')

def add_to_cart(request):
    # request.session.clear()
    print("request.session: ", request.session)
    print("request.POST: ", request.POST)
    print('request.POST["product_id"]: ', request.POST["product_id"])
    if "cart_dict" not in request.session:
        request.session["cart_dict"]={}
        request.session["quantity_in_cart"]=0
    if request.method == "POST":
        request.session["quantity_in_cart"]=0
        product_id = request.POST["product_id"]
        quantity = int(request.POST["quantity"])
        this_product = Product.objects.get(id=product_id)
        temp_quan_avail= this_product.temp_quan_avail
        if product_id in request.session["cart_dict"]:
            print("in line 113")
            if temp_quan_avail < quantity:
                print("in line 115")
                if temp_quan_avail == 0:
                    messages.error(request, f"Sorry, all we have left on this product is in your shopping cart. Please choose another product.")
                elif temp_quan_avail == 1:
                    messages.error(request, f"Sorry, we only have 1 item left. Please try to add 1  item to your cart.")
                elif temp_quan_avail > 1:
                    messages.error(request, f"Sorry, we only have {temp_quan_avail} items left. Please try to add up to {temp_quan_avail} items to your cart.")
                return redirect(request.META.get('HTTP_REFERER'))

            else: 
                print("in line 120")
                request.session["cart_dict"][product_id] += quantity
                old_quantity = request.session["quantity_in_cart"]
                new_quantity = old_quantity + quantity
                request.session["quantity_in_cart"] = new_quantity
                this_product.temp_quan_avail -= quantity
                this_product.save()

                return redirect('/success')
        else:
            print("in line 131")
            if temp_quan_avail < quantity:
                print("in line 130")
                if temp_quan_avail == 1:
                    messages.error(request, f"Sorry, we only have 1 item left. Please try to add 1 item to your cart.")
                elif temp_quan_avail > 1:
                    messages.error(request, f"Sorry, we only have {temp_quan_avail} items left. Please try to add up to {temp_quan_avail} items to your cart.")
                return redirect('/success')
            else:
                print("in line 137")
                request.session["cart_dict"][product_id] = quantity
                old_quantity = request.session["quantity_in_cart"]
                new_quantity = old_quantity + quantity
                request.session["quantity_in_cart"] = new_quantity
                this_product.temp_quan_avail -= quantity
                this_product.save()

                return redirect('/success')


    return redirect('/success')
    # return redirect('/')
    
def display_success(request):
    quantity_in_cart = 0
    for key in request.session["cart_dict"]:
        quantity_in_cart += request.session["cart_dict"][key]
    context = {
        "quantity_in_cart": quantity_in_cart,
    }
    return render(request, "_3_z_success.html", context)


def display_shopping_cart(request):
    pass
    # context = {
    #     "carts" : request.session["cart_dict"],
    #     "product_class": Product,
    # }
    # return render(request, "_4_shop_cart.html", context)
    return redirect('/')

def process_shopping_cart(request):
    pass
    # return redirect('/success')
    return redirect('/')

# search results views
class SearchResultsView(ListView):
    model = Product
    template_name = '_13_search_results.html'

    def get_queryset(self):
        query = self.request.GET.get('p')
        product_list = Product.objects.filter(Q(name__icontains=query))

        # context = {
        #     "product_list": Product.objects.filter(Q(name__icontains=query)),
        #     "all_photos": Photo.objects.all(),
        # }
        return product_list
    
    def get_context(self, request):
        all_photos = Photo.objects.all()
        
        return all_photos