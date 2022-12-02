from django import forms
from django.db.models import Count

from store.models import Product, Size


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'