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

        # if class_name == "cart":
            

        return errors


class Category(models.Model):
    name = models.CharField(max_length=255)
    cat_photo = models.ImageField(upload_to='categories', blank=True)
    #.products: multiple products could be in one category


class PhotoType(models.Model):
    name = models.CharField(max_length=255)
    #photos_included: one type of photo could include many photos



class Product(models.Model):
    name = models.CharField(max_length=255, default="")
    desc= models.TextField(default="")
    quantity_purchased = models.IntegerField(default=0)
    quantity_sold = models.IntegerField(default=0)
    quantity_available = models.IntegerField(default=0)
    temp_quan_avail = models.IntegerField(default=0)
    unit_price=models.DecimalField(max_digits=5, decimal_places=0)
    #photos: one product could have many photos. One photo is only for one product
    #included_in_orders: multiple products could be in one order, and multiple orders could be for one product

    category = models.ForeignKey(
        Category,
        related_name='products_included',
        on_delete=models.CASCADE
    )

    objects = ClassManager()
    def __str__(self):
        return self.name


class Photo(models.Model):   
    img = models.ImageField(upload_to='products', blank=True)

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
    # def __str__(self):
    #     return self.img



class Status(models.Model):
    name = models.CharField(max_length=255)
    #.order: multiple orders could have the same status
    


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
    # Email commented as it's not properly utilized currently
    # email = models.EmailField(max_length=255)

    orders_placed = models.ForeignKey(
        Order,
        related_name='customer_placed_by',
        on_delete=models.CASCADE
    )



class COA(models.Model):
    cash = models.DecimalField(max_digits=10, decimal_places=2)
    owner_investment = models.DecimalField(max_digits=10, decimal_places=2)
    sale_inc = models.DecimalField(max_digits=10, decimal_places=2)
    cost_of_sale = models.DecimalField(max_digits=10, decimal_places=2)
    overhead_exp = models.DecimalField(max_digits=10, decimal_places=2)

    #transactions: multiple transactions could affect one account, and multiple accounts could be included in one transaction

# class Cart(models.Model):
#     quantity_in_cart = models.IntegerField()
#     total_price = models.DecimalField(decimal_places=2)
#     product = models.ForeignKey(
#         Product,
#         related_name = "cart",
#         on_delete=models.CASCADE
#     )
#     customer = models.ForeignKey(
#         Customer,
#         related_name="carts",
#         on_delete=models.CASCADE
#     )

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



