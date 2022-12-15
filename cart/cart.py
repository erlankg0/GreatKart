from decimal import Decimal
from django.conf import settings
from store.models import Product, ProductVariant


# Корзина
class Cart(object):
    """Корзина"""

    def __init__(self, request):
        """Инициализация"""
        """(Конструктор корзины) Инициализация корзины"""
        self.session = request.session.get(
            settings.CART_SESSION_ID)  # получаем корзину из сессии (если есть) или создаем новую
        if not self.session:  # если корзины нет в сессии
            self.session = request.session[settings.CART_SESSION_ID] = {}  # создаем новую корзину в сессии
            self.cart = self.session  # корзина
        else:
            self.cart = self.session  # корзина (если есть в сессии) просто получаем ее

    def add(self, product_variant, quantity=1, update_quantity=False):
        """Добавление товара в корзину"""
        """(Метод add) Добавление товара в корзину"""
        product_variant_id = str(product_variant.id)  # получаем id товара
        if product_variant_id not in self.cart:
            self.cart[product_variant_id] = {'quantity': 0, 'price': str(
                product_variant.size.get_price_with_discount())}  # добавляем товар в корзину
        else:
            self.cart[product_variant_id][
                'quantity'] += quantity  # если товар уже есть в корзине, то увеличиваем количество
        self.save()  # сохраняем корзину

    def remove(self, product_variant):
        """Удаление товара из корзины"""
        """(Метод remove) Удаление товара из корзины"""
        product_variant_id = str(product_variant.id)
        if product_variant_id in self.cart:
            del self.cart[product_variant_id]
            self.save()

    def __iter__(self):
        """Итератор"""
        """(Метод __iter__) Итератор"""
        product_variant_ids = self.cart.keys()  # получаем id товаров по ключам словаря self.cart (корзины)
        product_variants = ProductVariant.objects.filter(
            id__in=product_variant_ids)  # получаем товары по id это список товаров
        for product_variant in product_variants:  # перебираем товары по списку
            self.cart[str(product_variant.id)][
                'product_variant'] = product_variant  # добавляем товар в корзину по ключу id

        for item in self.cart.values():  # перебираем значения словаря self.cart (корзины)
            item['price'] = Decimal(item['price'])  # цена товара
            item['total_price'] = item['price'] * item['quantity']  # общая цена товара
            yield item  # возвращаем значение общей цены товаров в корзине def get_total_price(self):

    def get_total_price(self):
        """Получение общей цены товаров в корзине"""
        """(Метод get_total_price) Получение общей цены товаров в корзине"""
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def save(self):
        """Сохранение корзины"""
        """(Метод save) Сохранение корзины"""
        self.session.modified = True
