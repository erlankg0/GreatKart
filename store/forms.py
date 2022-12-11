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


# ProductVariantForm - переопределяем форму __init__ для добавления измения size use FALSE
class ProductVariantForm(forms.ModelForm):
    class Meta:
        model = ProductVariant
        fields = ['product', 'size', 'color', 'image']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['size'].queryset = Size.objects.filter(Q(use=False), Q(price__lt=0))
