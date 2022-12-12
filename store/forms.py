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

    # переопределяем форму __init__ query_set для добавления измения size use FALSE
    def __init__(self, *args, **kwargs):
        super(ProductVariantForm, self).__init__(*args, **kwargs)
        self.fields['size'].queryset = Size.objects.filter(use=False)

    def clean(self):
        cleaned_data = super(ProductVariantForm, self).clean()
        product = cleaned_data.get('product')
        size = cleaned_data.get('size')
        color = cleaned_data.get('color')
        image = cleaned_data.get('image')
        if not product or not size or not color or not image:
            raise forms.ValidationError('Заполните все поля')
        return cleaned_data


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
