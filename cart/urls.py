from django.urls import path

"""Просмотры Views"""
from cart.views import cart, add_cart, remove_cart, remove_cart_item

"""Маршрутизатор URL"""
urlpatterns = [
    path('', cart, name='cart'),
    path('add_cart/<int:product_id>/', add_cart, name='add_cart'),
    path('remove/<int:product_id>/', remove_cart, name='remove_cart'),
    path('remove_item/<int:product_id>/', remove_cart_item, name='remove_item'),
]
