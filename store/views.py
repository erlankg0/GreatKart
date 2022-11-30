from django.shortcuts import render
from django.views.generic import ListView

from store.models import Product


class HomeView(ListView):
    model = Product
    context_object_name = 'products'
    template_name = 'store/index.html'


class ShopListView(ListView):
    model = Product
    context_object_name = 'products'
    template_name = None
    paginate_by = 9
