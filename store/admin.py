import admin_thumbnails
from django.contrib import admin
from django.utils.safestring import mark_safe
from django_mptt_admin.admin import DjangoMpttAdmin

from store.forms import ColorForm
from store.models import Product, CategoryMPTT, Brand, Size, Color, IP, Like, Images, Variants


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ('name',)}


@admin.register(Size)
class SizeAdmin(admin.ModelAdmin):
    pass


@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    form = ColorForm

    def display_color(self, obj):
        if obj.color:
            return mark_safe(
                f'<p style="background-color: {obj.name}; color: {obj.name};">{obj.name}</p>'
            )

    list_display = ['name', 'display_color', ]
    readonly_fields = ('name',)


@admin.register(IP)
class IPAdmin(admin.ModelAdmin):
    pass


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ('user',)}


@admin.register(CategoryMPTT)
class CategoryAdmin(DjangoMpttAdmin):
    prepopulated_fields = {'slug': ('title', 'parent',)}


class CategoryInline(admin.TabularInline):
    model = CategoryMPTT
    extra = 1


# admin_thumbnails -----------------------------------------------------------------------------------------------------
@admin_thumbnails.thumbnail('image')
class ProductImageInline(admin.TabularInline):
    model = Images
    readonly_fields = ('id',)
    extra = 1


class ProductVariantsInline(admin.TabularInline):
    model = Variants
    readonly_fields = ('image_tag',)
    extra = 1
    show_change_link = True


@admin_thumbnails.thumbnail('image')
@admin.register(Images)
class ImageAdmin(admin.ModelAdmin):
    list_display = ['image', 'id', 'name', 'image_thumbnail']


# Админ панель модели Product
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_available', 'image_tag']
    list_filter = ['category']
    readonly_fields = ('image_tag',)
    inlines = [ProductImageInline, ProductVariantsInline]
    prepopulated_fields = {"slug": ('name', 'keywords',)}


@admin.register(Variants)
class VariantsAdmin(admin.ModelAdmin):
    pass
