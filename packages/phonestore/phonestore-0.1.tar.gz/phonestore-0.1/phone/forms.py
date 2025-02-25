

from pyexpat import model
import django
from django.forms import ModelForm,widgets
from .models import Product
from django import forms


class ProductForm(ModelForm):

    class Meta:

        model = Product
        fields = ['Product_name', 'description',
                  'image', 'Price', 'Stock', 'category']

        widgets = {
            'tags': forms.CheckboxSelectMultiple(),

        }


def __init__(self, *args, **kwargs):

    super(ProductForm, self).__init__(*args, **kwargs)

    self.fields['Product_name'].widget.attrs.update(
        {'class': 'form-control form-control-user', 'placeholder': 'Product Name'})

    self.fields['description'].widget.attrs.update(
        {'class': 'form-control form-control-user', 'placeholder': 'Add  description'})
    self.fields['image'].widget.attrs.update(
        {'class': 'form-control form-control-user', 'placeholder': 'Add  image'})
    self.fields['Price'].widget.attrs.update(
        {'class': 'form-control form-control-user', 'placeholder': 'Add  Price'})
    self.fields['Stock'].widget.attrs.update(
        {'class': 'form-control form-control-user', 'placeholder': 'Add  Stock'})
    self.fields['category'].widget.attrs.update(
        {'class': 'form-control form-control-user', 'placeholder': 'Add  category'})
