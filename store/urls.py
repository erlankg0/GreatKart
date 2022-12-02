from django.urls import path

"""Просмотры (Views) """
from store.views import HomeView, ShopListView, ShopByCategoryListView, DetailProduct, forms

"""Маршрутизатор URL"""
urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('shop/', ShopListView.as_view(), name='shop'),
    path('shop/category/<slug:slug>/', ShopByCategoryListView.as_view(), name='shop_by_category'),
    path('shop/product/<slug:product_slug>/', DetailProduct.as_view(),
         name='detail_product'),
    path('shop/forms/', forms),
]
