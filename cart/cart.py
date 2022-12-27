from decimal import Decimal
from django.conf import settings
from store.models import Product, ProductVariant


class Cart:
    """Класс корзины"""

    def __init__(self, request):
        """Инициализация корзины"""
        self.session = request.session  # получаем сессию
        cart = self.session.get(settings.CART_SESSION_ID)  # получаем корзину из сессии или создаем новую корзину
        print('Cart init: cart = {}'.format(cart))
        if not cart:  # если корзины нет, то создаем ее
            cart = self.session[
                settings.CART_SESSION_ID] = {}  # создаем корзину в сессии и присваиваем ее переменной cart
        self.cart = cart  # присваиваем корзину атрибуту класса

    def add(self, product, product_variant=None, quantity=1, update_quantity=False):
        """Добавление товара в корзину"""
        product_id = str(product.id)  # получаем id товара
        product_variant_id = str(product_variant.id) if product_variant else None  # получаем id варианта товара
        if product_id not in self.cart:  # если товара нет в корзине, то добавляем его
            self.cart[product_id] = {'quantity': 0, 'price': str(product.price)}
        if product_variant_id:
            if 'variants' not in self.cart[product_id]:
                self.cart[product_id]['variants'] = {}  # создаем словарь вариантов товара
            if product_variant_id not in self.cart[product_id][
                'variants']:  # если варианта товара нет в корзине, то добавляем его
                self.cart[product_id]['variants'][product_variant_id] = {'quantity': 0,
                                                                         'price': str(product_variant.price)
                                                                         }  # добавляем вариант товара в корзину
            if update_quantity:  # если нужно обновить количество товара
                self.cart[product_id]['variants'][product_variant_id][
                    'quantity'] = quantity  # обновляем количество товара
            else:  # если нужно добавить количество товара
                self.cart[product_id]['variants'][product_variant_id][
                    'quantity'] += quantity  # увеличиваем количество товара
                self.save()

    def save(self):
        """Сохранение корзины"""
        # обновляем сессию cart
        self.session[settings.CART_SESSION_ID] = self.cart
        # помечаем сессию как "измененную", чтобы убедиться, что она будет сохранена
        self.session.modified = True

    def remove(self, product):
        """Удаление товара из корзины"""
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def __iter__(self):
        """Итерация по товарам в корзине"""
        product_ids = self.cart.keys()
        # получаем объекты модели Product и передаем их в корзину
        products = Product.objects.filter(id__in=product_ids)
        for product in products:
            self.cart[str(product.id)]['product'] = product

        for item in self.cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        """Подсчет количества товаров в корзине"""
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        """Подсчет общей стоимости товаров в корзине"""
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def clear(self):
        """Очистка корзины"""
        # удаление корзины из сессии
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True
