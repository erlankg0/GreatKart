from django.db import models

from store.models import Product


class Cart(models.Model):
    """Модель корзины товаров"""
    cart_id = models.CharField(
        max_length=255,
        blank=True,
    )
    date_added = models.DateTimeField(
        auto_now_add=True,
    )

    def __str__(self):
        return self.cart_id


class CartItem(models.Model):
    """Модель товара из корзины"""
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE
    )
    quantity = models.PositiveIntegerField()
    is_active = models.BooleanField(
        default=True
    )

    def total_price(self):
        return self.product.price * self.quantity

    def __unicode__(self):
        return self.product
