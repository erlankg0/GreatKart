from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect, render, get_object_or_404

from cart.models import Cart, CartItem
from store.models import Product


# get session KEY
def _cart_id(request):
    # забирает ключ сессии (get session key)
    cart = request.session.session_key
    # проверка есть ли сессия if have not session
    if not cart:  # если нету тогда сделаем сессию / create new session
        cart = request.session.create()
    return cart


# Add to Cart
def add_cart(request, product_id):
    product = Product.objects.get(id=product_id)  # получаем продукт (get item)
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))  # get the cart using the cart_id present in the session
    except Cart.DoesNotExist:
        cart = Cart.objects.create(
            cart_id=_cart_id(request)
        )
    cart.save()

    try:
        cart_item = CartItem.objects.get(
            product_id=product,
            cart_id=cart
        )
        cart_item.quantity += 1  # + 1
        cart_item.save()
    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(
            product=product,
            quantity=1,
            cart=cart,
        )
        cart_item.save()
    return redirect('cart')


# remove item in cart
def remove_cart(request, product_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))  # get current cart
    product = Product.objects.get(product_id=product_id)
    cart_item = CartItem.objects.get(
        cart=cart,
        product=product
    )
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cart')


def remove_cart_item(request, product_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product, id=1)
    cart_item = CartItem(product=product, cart=cart)
    cart_item.delete()
    return redirect('cart')


# View cart in HTML
def cart(request, total=0, quantity=0, cart_items=None):
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for item in cart_items:
            total += (item.product.price * item.quantity)  # total all item price
            quantity += item.quantity  # total all item.quantity
    except ObjectDoesNotExist:
        pass  # just ignore
    tax = total * 0.18
    grand_total = total + tax
    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax': tax,
        'grand_total': grand_total

    }
    return render(request, 'cart/cart.html', context)
