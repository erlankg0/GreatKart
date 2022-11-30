from django.contrib import admin
from django.utils.safestring import mark_safe

from store.models import Product


# Админ панель модели Product
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Панель администрации измененный """
    list_display = ('name', 'get_image', 'price', 'stock', 'modified_date', 'is_available',)
    list_filter = ('name', 'price', 'stock', 'modified_date', 'is_available',)
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ('price', 'stock',)

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
