from django.db import models

# Create your models here.

from Accounts.models import Account
from phone.models import Product
from card.models import Variations


class Payement(models.Model):

    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    payement_id = models.CharField(max_length=100)
    payement_method = models.CharField(max_length=100)
    amount_paid = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):

        return self.payement_id


class Order(models.Model):

    STATUS = {
        ('New', 'New'),
        ('Accepted', 'accepted'),
        ('Completed', 'Completed'),
        ('Cenceled', 'Cenceled'),

    }

    user = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True)
    payement = models.ForeignKey(
        Payement, on_delete=models.SET_NULL, blank=True, null=True)
    order_number = models.CharField(max_length=20)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=15)
    email = models.EmailField(max_length=50)
    adress_line_1 = models.CharField(max_length=50)
    adress_line_2 = models.CharField(max_length=50, blank=True)
    country = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    order_note = models.CharField(max_length=100, blank=True)

    order_total = models.FloatField()

    tax = models.FloatField()

    status = models.CharField(max_length=10, choices=STATUS, default='New')

    ip = models.CharField(max_length=20, blank=True)

    is_ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    uploaded_at = models.DateTimeField(auto_now=True)

    def __str__(self):

        return self.first_name


class OrderProduct(models.Model):

    order = models.ForeignKey(Order, on_delete=models.CASCADE)

    user = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True)

    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)

    product_owner = models.ForeignKey(Account,on_delete=models.CASCADE, related_name="ownerproduct")

    variation = models.ManyToManyField(Variations, blank=True)
    
    quantity = models.IntegerField()

    product_price = models.FloatField()

    ordered = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    uploaded_at = models.DateTimeField(auto_now=True)

    def __str__(self):

        return self.product.Product_name
