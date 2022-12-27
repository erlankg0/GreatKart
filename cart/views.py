from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.views.decorators.http import require_POST  # декоратор для обработки POST запросов
from store.models import Product  # импортируем модель Product
from .cart import Cart  # импортируем класс корзины
from .forms import CartAddProductForm  # импортируем форму


@require_POST  # декоратор для обработки POST запросов
def cart_add(request, product):
    cart = Cart(request)  # создаем объект корзины с текущим запросом request
    product = get_object_or_404(Product, id=product)  # получаем товар по id
    print(product)
    form = CartAddProductForm(request.POST)  # создаем объект формы с данными из POST запроса
    if form.is_valid():
        print('form.is_valid')
        cd = form.cleaned_data  # получаем данные из формы
        cart.add(
            product=product,
            quantity=cd['quantity'],
            update_quantity=cd['update']
        )  # добавляем товар в корзину
        return redirect('cart_detail')  # перенаправляем на страницу корзины


def cart_remove(request, product_id):
    cart = Cart(request)  # создаем объект корзины с текущим запросом request
    product = get_object_or_404(Product, id=product_id)  # получаем товар по id
    cart.remove(product)  # удаляем товар из корзины
    return redirect('cart_detail')  # перенаправляем на страницу корзины


def cart_detail(request):
    cart = Cart(request)  # создаем объект корзины с текущим запросом request
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(
            initial={'quantity': item['quantity'],
                     'update': True}
        )
    return render(request, 'cart/cart.html', {'cart': cart.cart})
