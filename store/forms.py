from django import forms

from store.models import Product, Color


class ColorForm(forms.ModelForm):
    class Meta:
        model = Color
        fields = ('name', 'color')

        widgets = {
            'color': forms.TextInput(
                attrs={
                    "type": 'color',
                }
            )
        }


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
