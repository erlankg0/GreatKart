from django import forms


# форма для добавления товара в корзину
class CartAddProductForm(forms.Form):
    quantity = forms.IntegerField(
        label='Количество',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'type': 'number',
                'value': '1',
                'min': '1'
            }
        )
    ) # поле для количества товара в корзине (по умолчанию 1)
    update = forms.BooleanField(
        required=False,  # не обязательное поле
        initial=False,  # начальное значение
        widget=forms.HiddenInput  # виджет для скрытого поля

    )  # поле для обновления товара в корзине
