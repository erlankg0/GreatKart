from django.contrib import admin
from django.utils.safestring import mark_safe

from store.models import Product, CategoryMPTT, Brand, Size, Color, Quantity, IP, Like, Image
from store.forms import ProductForm


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    pass


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ('name',)}


@admin.register(Size)
class SizeAdmin(admin.ModelAdmin):
    pass


@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    pass


@admin.register(Quantity)
class QuantityAdmin(admin.ModelAdmin):
    pass


@admin.register(IP)
class IPAdmin(admin.ModelAdmin):
    pass


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ('user',)}


@admin.register(CategoryMPTT)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title', 'parent',)}


# Админ панель модели Product
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Панель администрации измененный """
    form = ProductForm

    def get_image(self, obj):
        """
        obj -> Product
        проверяем если в Product.images есть изображение
        тогда через функцию mark_safe выводим в админ панели изоброжения продукта.
        А если нету тогда просто дефиз
        """
        if obj.images:
            return mark_safe(f'<img src="{obj.images.url}" alt="{obj.name}" width="60">')
        else:
            return mark_safe("-")

    get_image.__name__ = 'Изображение'
    list_display = ('name', 'price', 'discount_price', 'stock', 'modified_date', 'is_available',)
    list_filter = ('name', 'price', 'discount_price', 'stock', 'modified_date', 'is_available',)
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ('price', 'discount_price', 'stock',)
