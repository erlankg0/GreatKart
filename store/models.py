from django.db import models
from django.urls import reverse

from category.models import Category
from store.utils import directory_path


class Product(models.Model):
    """SQL модель товара(продукта)"""
    name = models.CharField(
        max_length=200,
        unique=True,
        verbose_name='Название продукта',
        help_text='Максимальная длина 200 симвлов и должна быть уникальной'
    )
    description = models.TextField(
        max_length=450,
        verbose_name='Описание товара',
        help_text='Максимальная длина 450 символов может быть пустая',
    )
    slug = models.SlugField(
        max_length=200,
        unique=True,
        verbose_name='URL',
        help_text='Максимальная длина 200 симвлов и должна быть уникальной',
    )
    price = models.PositiveIntegerField(
        verbose_name='Цена',
        help_text='Только позитивные числа'
    )
    discount = models.BooleanField(
        default=False,
        verbose_name='Скидка'
    )
    discount_price = models.PositiveIntegerField(
        verbose_name='Скидка',
        help_text='Пишем сумму скидки'
    )
    images = models.ImageField(
        verbose_name='Изображение продукта',
        help_text='Изображение категории',
        upload_to=directory_path,
        blank=True,
        null=True
    )
    stock = models.PositiveIntegerField(
        verbose_name='Колличество в складе'
    )
    is_available = models.BooleanField(
        default=False,
        verbose_name='В продаже',
        help_text='В продаже, если в складе не осталось будет убрана с продажи'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        verbose_name='Категория товара',
        help_text='Удаляется товар если удалится категория'
    )
    created_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата и время поставки товара на склад',
        help_text="Автоматически сохраняет дату и время"
    )
    modified_date = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата и время изменения',
        help_text="Автоматически уставливается"
    )

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('detail_product', args=[self.category.slug, self.slug])

    def save(self, *args, **kwargs):
        if self.discount:
            self.price = self.price - self.discount_price
        super(Product, self).save(*args, **kwargs)

    class Meta:
        ordering = ['-name', ]
        db_table = 'products'
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
