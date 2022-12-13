from django.contrib import admin

from store.forms import ProductVariantForm, ColorForm
from store.models import CategoryMPTT, Brand, Product, ProductVariant, Ip, Size, Color, Like, Image, Review


@admin.register(CategoryMPTT)
class CategoryMPTTAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


class ProductVariantInline(admin.StackedInline):
    form = ProductVariantForm
    model = ProductVariant
    extra = 1


class ImageInline(admin.TabularInline):
    model = Image
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ImageInline, ProductVariantInline]


@admin.register(ProductVariant)
class ProductVariantAdmin(admin.ModelAdmin):
    form = ProductVariantForm


@admin.register(Ip)
class IpAdmin(admin.ModelAdmin):
    pass


@admin.register(Size)
class SizeAdmin(admin.ModelAdmin):
    pass


@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    form = ColorForm


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    pass


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    pass


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    pass
