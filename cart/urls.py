from django.urls import path

"""Просмотры Views"""
from .views import cart_add, cart_remove, cart_detail

"""Маршрутизатор URL"""
urlpatterns = [
    path('', cart_detail, name='cart_detail'),
    path('add/<int:product>/', cart_add, name='cart_add'),
    path('remove/<int:product_id>/', cart_remove, name='cart_remove'),
]
