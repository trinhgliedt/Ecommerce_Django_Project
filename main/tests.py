from django.db import models
import re

# Create your models here.
class ClassManager(models.Manager):
    def basic_validator(self, post_data, class_name):
        errors = {}
        if class_name == "employee":
            EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+[a-zA-Z]+$')

            if len(post_data["first_name"]) < 2:
                errors["first_name"] = "Please enter at least 2 characters for your first name."
            if len(post_data["last_name"]) < 2:
                errors["last_name"] = "Please enter at least 2 characters for your last name."
            if not EMAIL_REGEX.match(post_data['email']): 
                errors['email'] = 'Please enter a valid email address!'
            elif User.objects.filter(email = post_data["email"]).exists():
                errors['email'] = "You can't use that email address."
            if len(post_data["password"]) < 6:
                errors["password"] = "Please enter at least 6 characters for your password."
            else:
                if post_data["password"] != post_data["confirmPW"]:
                    errors["confirmPW"] = "Please ensure that your password matches the confirmation."

        # if class_name == "job":
        #     if len(post_data["tittle"]) < 1:
        #         errors["tittle"] = "Please enter a tittle for the job."
        #     elif len(post_data["tittle"]) < 3:
        #         errors["tittle"] = "Please enter at least 3 characters for the job tittle."
            
        #     if len(post_data["desc"]) < 1:
        #         errors["desc"] = "Please enter a description for the job."
        #     elif len(post_data["desc"]) < 3:
        #         errors["desc"] = "Please enter at least 3 characters for the job description."
           
        #     if len(post_data["location"]) < 1:
        #         errors["location"] = "Please enter a location for the job."   
        #     elif len(post_data["location"]) < 3:
        #         errors["location"] = "Please enter at least 3 characters for the job description."

        return errors


class Category(models.Model):
    name = models.CharField(max_length=255)
    #.products: multiple products could be in one category
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

class PhotoType(models.Model):
    name = models.CharField(max_length=255)
    #photos_included: one type of photo could include many photos
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)


class Product(models.Model):
    name = models.CharField(max_length=255)
    desc= models.TextField()
    quantity_purchased = models.IntegerField()
    quantity_sold = models.IntegerField()
    unit_price=models.DecimalField(max_digits=5, decimal_places=2)
    #photos: one product could have many photos. One photo is only for one product
    #included_in_orders: multiple products could be in one order, and multiple orders could be for one product

    category = models.ForeignKey(
        Category,
        related_name='products_included',
        on_delete=models.CASCADE
    )

    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

class Photo(models.Model):   
    name = models.ImageField(upload_to='images/products')

    type_of_photo = models.ForeignKey(
        PhotoType,
        related_name='photos_included',
        on_delete=models.CASCADE
    )
    for_product = models.ForeignKey(
        Product,
        related_name='photos',
        on_delete=models.CASCADE
    )

    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)


class Status(models.Model):
    name = models.CharField(max_length=255)
    #.order: multiple orders could have the same status
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)


class Order(models.Model):
    status = models.ForeignKey(
        Status,
        related_name='order',
        on_delete=models.CASCADE
    )
    total_product_price = models.DecimalField(max_digits=5, decimal_places=2)
    shipping_fee = models.DecimalField(max_digits=5, decimal_places=2)
    #customer_placed_by: one customer could place multiple orders

    products_included = models.ManyToManyField(
        Product,
        related_name='included_in_orders',
    )

    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

class Customer(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    address_street  = models.CharField(max_length=255)
    address_city  = models.CharField(max_length=45)
    address_state  = models.CharField(max_length=2)
    address_zipcode  = models.CharField(max_length=5)
    email = models.EmailField(max_length=255)

    orders_placed = models.ForeignKey(
        Product,
        related_name='customer_placed_by',
        on_delete=models.CASCADE
    )

    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

class COA(models.Model):
    cash = models.DecimalField(max_digits=10, decimal_places=2)
    owner_investment = models.DecimalField(max_digits=10, decimal_places=2)
    sale_inc = models.DecimalField(max_digits=10, decimal_places=2)
    cost_of_sale = models.DecimalField(max_digits=10, decimal_places=2)
    overhead_exp = models.DecimalField(max_digits=10, decimal_places=2)

    #transactions: multiple transactions could affect one account, and multiple accounts could be included in one transaction

    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

class Transaction(models.Model):
    #accounts: one transaction could have multiple accounts, and one account could be affected by multiple transactions
    trans_type = models.CharField(max_length=6) 

    accounts = models.ManyToManyField(
        COA,
        related_name='transactions',
    )

    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

class UserGroup(models.Model):
    name = models.CharField(max_length=255)
    #employees_included: one user group could have multiple employees

class Employee(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    password = models.CharField(max_length=64)

    group = models.ForeignKey(
        UserGroup,
        related_name='employees_included',
        on_delete=models.CASCADE
    )

    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

