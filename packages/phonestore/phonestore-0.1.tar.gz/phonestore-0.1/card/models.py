from django.db import models


from Accounts.models import Account

from phone.models import Product

import uuid

# Create your models here.


class VariationManager(models.Manager):
    def colors(self):

        return super(VariationManager, self).filter(variation_category='color')

    def sizes(self):

        return super(VariationManager, self).filter(variation_category='size')


variation_category_choice = (
    ('color', 'color'),

    ('size', 'size'),

)


class Variations(models.Model):

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variation_category = models.CharField(
        max_length=100, choices=variation_category_choice)

    variation_value = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now=True)

    objects = VariationManager()

    def __str__(self):

        return self.product.Product_name + "    " + self.variation_value


class CardItem(models.Model):

    owner = models.ForeignKey(Account, on_delete=models.CASCADE)

    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)

    variation = models.ManyToManyField(Variations, blank=True)

    quantity = models.IntegerField()

    totals = models.FloatField()

    is_active = models.BooleanField(default=True)

    created = models.DateTimeField(auto_now_add=True)

    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)

    def __str__(self):

        return self.product.Product_name
