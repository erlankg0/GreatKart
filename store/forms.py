from django import forms
from store.models import Product, ProductVariant, CategoryMPTT, Brand, Size, Color
from django.db.models import Q


class ColorForm(forms.ModelForm):
    class Meta:
        model = Color
        fields = ['color']

        widgets = {
            'color': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Введите цвет',
                    'type': 'color',
                }
            )
        }


class ProductVariantForm(forms.ModelForm):
    class Meta:
        model = ProductVariant
        fields = ['product', 'size', 'color', 'image']

    def clean(self):
        cleaned_data = super().clean()
        product = cleaned_data.get('product')
        size = cleaned_data.get('size')
        color = cleaned_data.get('color')
        if ProductVariant.objects.filter(size__in=size):  # если есть такой размер
            raise forms.ValidationError('Такой вариант уже существует в добавьте уникальный размер')
        if ProductVariant.objects.filter(product=product, color=color):
            raise forms.ValidationError('Такой вариант уже существует в добавьте уникальный цвет')



class SizeForm(forms.ModelForm):
    class Meta:
        model = Size
        fields = ['size']

        widgets = {
            'size': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Введите размер',
                }
            )
        }
