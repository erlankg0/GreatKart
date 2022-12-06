from django.db import models
from django.urls import reverse
from mptt.models import TreeForeignKey, MPTTModel

from store.utils import directory_image_path, get_sizes
from accounts.models import Account

"""
Модели SQL

Category

Size

Color

Quantity

Images

IP

Like

Brand

Product

"""


class CategoryMPTT(MPTTModel):
    """Категория продукта"""
    title = models.CharField(
        max_length=50,
        unique=True,
        verbose_name='Название категории'
    )
    parent = TreeForeignKey(
        'self',
        on_delete=models.PROTECT,
        related_name='children',
        blank=True, null=True,
        db_index=True,
        verbose_name='Подкатегория'
    )
    slug = models.SlugField(
        unique=True
    )

    def __str__(self):
        full_path = [self.title]
        k = self.parent
        while k is not None:
            full_path.append(k.title)
            k = k.parent
        return ' -> '.join(full_path[::-1])

    def get_absolute_url(self):
        return reverse('shop_by_category', kwargs={'slug': self.slug})

    class MPTTMeta:
        order_insertion_by = ['title']

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        db_table = 'category_mptt'  # Имя таблицы


class Image(models.Model):
    name = models.CharField(
        verbose_name='Название картинки',
        max_length=155,
    )
    image = models.ImageField(
        upload_to='images/',
        verbose_name='Картинка'
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Картинка'
        verbose_name_plural = 'Картинки'
        db_table = 'image'  # Имя таблицы


class IP(models.Model):
    ip = models.CharField(
        verbose_name='Тут хранится IP адреса',
        max_length=50,
        unique=True,
    )

    def __str__(self):
        return self.ip

    class Meta:
        db_table = 'customer_ip'  # Имя таблицы
        verbose_name = 'IP'
        verbose_name_plural = 'IP'


class Like(models.Model):
    user = models.ForeignKey(
        Account,
        on_delete=models.CASCADE,
        verbose_name='Нравится'
    )

    slug = models.SlugField()

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = 'Нравится'
        verbose_name_plural = 'Нравится'
        db_table = 'like'  # Имя таблицы


class Size(models.Model):
    """Размер продукта"""
    size = models.CharField(
        max_length=10,
        choices=get_sizes()
    )

    def __str__(self):
        return self.size

    class Meta:
        verbose_name = 'Размер'
        verbose_name_plural = 'Размеры'
        db_table = 'size'  # Имя таблицы


class Color(models.Model):
    """Таблица для хранения цветов товаров"""
    COLOR = (
        ('BLACK', 'BLACK'),
        ('WHITE', 'WHITE'),
        ('GRAY', 'GRAY'),
        ('BEIGE', 'BEIGE'),
        ('RED', 'RED'),
        ('BLUE', 'BLUE'),
    )
    color = models.CharField(
        max_length=10,
        verbose_name='Цвет товара',
        choices=COLOR,
    )
    slug = models.SlugField(
        verbose_name='URL'
    )

    def __str__(self):
        return self.color

    class Meta:
        verbose_name = 'Цвет товар'
        verbose_name_plural = 'Цвета товаров'
        db_table = 'color'  # Имя таблицы


class Quantity(models.Model):
    """Таблица для хранения колличество товаров"""
    quantity = models.PositiveIntegerField(
        verbose_name='Колличество товара'
    )
    slug = models.SlugField(
        verbose_name='URL'
    )

    def __str__(self):
        return str(self.quantity)

    class Meta:
        verbose_name = 'Колличество товара'
        verbose_name_plural = 'Колличество товаров'
        db_table = 'quantity'  # Имя таблицы


class Brand(models.Model):
    name = models.CharField(
        max_length=155,
        verbose_name='Названия бренда',
        help_text='Максимум 155 символов, уникальное',
        unique=True,
    )
    slug = models.SlugField(
        max_length=155,
        verbose_name='URL',
        help_text='Максимум 155 символов, уникальное',
        unique=True,
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Бренд'
        verbose_name_plural = 'Бренды'
        db_table = 'brand'  # Имя таблицы


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
    brand = models.OneToOneField(
        Brand,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    category = models.ManyToManyField(
        CategoryMPTT,
        verbose_name='Категория товара',
        help_text='Удаляется товар если удалится категория',
        related_name='products'
    )
    images = models.ManyToManyField(
        Image,
        verbose_name='Изображение продукта',
    )
    size = models.ForeignKey(
        Size,
        on_delete=models.PROTECT,
        verbose_name='Размер',
    )
    color = models.ForeignKey(
        Color,
        on_delete=models.PROTECT,
        verbose_name='Цвет'
    ),
    quantity = models.OneToOneField(
        Quantity,
        on_delete=models.PROTECT,
        verbose_name='Колличество'
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
        help_text='Пишем сумму скидки',
        blank=True,
        null=True,
    )
    discounted = models.PositiveIntegerField(
        verbose_name='Старая цена',
        help_text='Если есть скидка тут будет хранится старая цена',
        blank=True,
        null=True,
    )
    stock = models.PositiveIntegerField(
        verbose_name='Колличество в складе'
    )
    sold = models.PositiveIntegerField(
        verbose_name='Продано',
        blank=True,
        default=0
    )
    is_available = models.BooleanField(
        default=False,
        verbose_name='В продаже',
        help_text='В продаже, если в складе не осталось будет убрана с продажи'
    )
    view = models.ForeignKey(
        IP,
        on_delete=models.CASCADE,
        verbose_name='Просмотры',
        blank=True,
        null=True,
    )
    like = models.ForeignKey(
        Like,
        on_delete=models.CASCADE,
        verbose_name='Нравится',
        blank=True,
        null=True,
    )
    slug = models.SlugField(
        max_length=200,
        unique=True,
        verbose_name='URL',
        help_text='Максимальная длина 200 симвлов и должна быть уникальной',
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
        return reverse('detail_product', args=[self.slug])

    def liked_count(self):
        return self.like.count()

    def save(self, *args, **kwargs):
        if self.discount:
            self.discounted = self.price + self.discount_price
        super(Product, self).save(*args, **kwargs)

    class Meta:
        ordering = ['-name', ]
        db_table = 'products'  # Имя таблицы
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
