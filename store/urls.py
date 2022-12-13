from django.urls import path

"""Просмотры (Views) """
from store.views import HomeView, DetailProduct
from store.views import ShopListView, ShopByCategoryListView, ShopByBrandListView
from store.views import get_size, get_price, add_like

"""Маршрутизатор URL"""
urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('shop/', ShopListView.as_view(), name='shop'),
    path('shop/category/<slug:slug>/', ShopByCategoryListView.as_view(), name='shop_by_category'),
    path('shop/brand/<slug:slug>/', ShopByBrandListView.as_view(), name='shot_by_brand'),
    path('shop/product/<slug:product_slug>/', DetailProduct.as_view(),
         name='detail_product'),
    # AJAX
    path('shop/variant/<int:variant_id>/', get_size, name='get_variants'),
    path('shop/size/<int:size_id>/price/quantity/', get_price, name='get_price'),
    path('shop/like/<int:product_id>/<str:ip_address>/', add_like, name='add_like'),
]
