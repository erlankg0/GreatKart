import requests
from django.db import models
from django.urls import reverse
from accounts.models import Account
from store.utils import directory_image_path
from mptt.models import TreeForeignKey, MPTTModel


class CategoryMPTT(MPTTModel):
    """Product category"""
    title = models.CharField(
        max_length=50,
        unique=True,
        verbose_name='Category name'
    )  # Category name
    parent = TreeForeignKey(
        'self',
        on_delete=models.PROTECT,
        related_name='children',
        blank=True, null=True,
        db_index=True,
        verbose_name='Subcategory'
    )  # Category slug
    slug = models.SlugField(
        unique=True
    )

    def __str__(self):
        full_path = [self.title]
        k = self.parent
        while k is not None:
            full_path.append(k.title)
            k = k.parent
        return ' -> '.join(full_path[::-1])  # Return category name

    def get_absolute_url(self):  # Return category slug
        return reverse('shop_by_category', kwargs={'slug': self.slug})

    class MPTTMeta:
        order_insertion_by = ['title']  # Order by title

    class Meta:  # Meta class
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        db_table = 'category_mptt'  # Table name


class Brand(models.Model):  # Brand
    name = models.CharField(
        max_length=100,
        verbose_name='Brand name',
        help_text='Max 100 symbols, unique e.g. "Nike"',
        unique=True,
    )  # Название бренда
    slug = models.SlugField(
        max_length=100,
        verbose_name='URL',
        help_text='Max 100 symbols, unique e.g. "nike"',
        unique=True,
    )  # URL бренда

    def get_absolute_url(self):  # Возвращает абсолютный URL бренда
        return reverse('shot_by_brand', kwargs={"slug": self.slug})

    def __str__(self):  # Возвращает название бренда
        return self.name

    class Meta:
        verbose_name = 'Бренд'  # Имя модели
        verbose_name_plural = 'Бренды'  # Имя модели во множественном числе
        db_table = 'brand'  # Имя таблицы
        ordering = ['name']  # Сортировка по названию бренда


# Модель Ip адреса
class Ip(models.Model):
    ip = models.GenericIPAddressField(
        verbose_name='IP address',
        help_text='IP address',
        unique=True,
    )  # IP адрес

    def __str__(self):  # Возвращает IP адрес
        return self.ip

    class Meta:
        verbose_name = 'IP адрес'  # Имя модели
        verbose_name_plural = 'IP адреса'  # Имя модели во множественном числе
        db_table = 'ip'  # Имя таблицы


# Модель каринки
class Image(models.Model):
    image = models.ImageField(
        upload_to='images/',
        verbose_name='Image',
        help_text='Image',
    )  # Картинка
    product = models.ForeignKey(
        'Product',
        on_delete=models.CASCADE,
        related_name='images_product',
        verbose_name='Product',
        help_text='Image',
        blank=True,
        null=True,

    )  # Продукт

    class Meta:
        verbose_name = 'Картинка'  # Имя модели
        verbose_name_plural = 'Картинки'  # Имя модели во множественном числе
        db_table = 'image'  # Имя таблицы


# Модель Like
class Like(models.Model):
    ip = models.ForeignKey(
        Ip,
        on_delete=models.CASCADE,
        verbose_name='IP address',
        help_text='IP address',
    )  # IP адрес
    product = models.ForeignKey(
        'Product',
        on_delete=models.CASCADE,
        verbose_name='Product',
        help_text='Product',
    )  # Продукт

    def __str__(self):  # Возвращает IP адрес и продукт
        return f'{self.ip} - {self.product}'

    class Meta:
        verbose_name = 'Нравится'  # Имя модели
        verbose_name_plural = 'Нравится'  # Имя модели во множественном числе
        db_table = 'like'  # Имя таблицы


# Product model  category is many to many field commented on english
class Product(models.Model):
    """Product"""
    category = models.ManyToManyField(
        CategoryMPTT,
        verbose_name='Category',
        related_name='products',
    )  # Категория
    brand = models.ForeignKey(
        Brand,
        on_delete=models.PROTECT,
        verbose_name='Brand',
        related_name='products',
    )  # Бренд
    title = models.CharField(
        max_length=100,
        verbose_name='Product name',
        help_text='Max 100 symbols, unique e.g. "Nike Air Max 270"',
        unique=True,
    )  # Название продукта
    description = models.TextField(
        verbose_name='Description',
        help_text='Description',
    )  # Описание
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Regular price',
        help_text='Regular price Nike Air Max 270 100$',
        default=0,
    )  # Цена
    image = models.ImageField(
        upload_to=directory_image_path,
        verbose_name='Image',
        help_text='Image',
    )  # Картинка
    view = models.ManyToManyField(
        Ip,  # Ip адрес
        verbose_name='View',  # Просмотр
        related_name='view_products',  # related_name='view_products'
        help_text='view count',  # Просмотры
        blank=True,
        null=True,
    )  # View
    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Created',
        help_text='Created',
    )  # Дата создания
    updated = models.DateTimeField(
        auto_now=True,
        verbose_name='Updated',
        help_text='Updated',
    )  # Дата обновления
    is_active = models.BooleanField(
        default=True,
        verbose_name='Is active',
        help_text='Is active',
    )  # Активный
    is_new = models.BooleanField(
        default=False,
        verbose_name='Is new',
        help_text='Is new Nike Air Max 270',
    )  # Новый
    is_deleted = models.BooleanField(
        default=False,  # Удален
        verbose_name='Is deleted',  # Удален
        help_text='Is deleted',  # Удален
    )  # Удаленный
    slug = models.SlugField(
        max_length=100,  # Максимальная длина 100 символов
        verbose_name='URL',  # URL
        help_text='Max 100 symbols, unique e.g. "nike-air-max-270"',  # URL
        unique=True,
    )  # URL продукта

    def get_absolute_url(self):  # Возвращает абсолютный URL продукта
        return reverse('detail_product', args=[self.slug])

    def get_new_products(self):  # Возвращает новые продукты
        return self.objects.filter(is_new=True).order_by('-created')

    def get_view_count(self):  # Возвращает количество просмотров
        return self.view.count()

    def get_popular_products(self):  # Возвращает популярные продукты
        return self.objects.filter(is_active=True).order_by('-view')

    def __str__(self):  # Возвращает название продукта
        return self.title

    class Meta:
        verbose_name = 'Продукт'  # Имя модели
        verbose_name_plural = 'Продукты'  # Имя модели во множественном числе
        db_table = 'product'


# Модель размера с количеством
class Size(models.Model):
    size = models.CharField(
        max_length=255,
        verbose_name='Size',
        help_text='Size',
    )  # Размер
    quantity = models.IntegerField(
        verbose_name='Quantity',
        help_text='Quantity',
    )  # Количество
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Price',
        help_text='Price',
    )  # Цена
    discount = models.PositiveSmallIntegerField(
        default=0,
        verbose_name='Discount',
        help_text='Discount',
    )  # Скидка
    use = models.BooleanField(
        default=True,
        verbose_name='Used',
        help_text='Used',
    )  # Используется

    def get_price_with_discount(self):  # Возвращает цену с учетом скидки
        return self.price - (self.price * self.discount / 100)

    def __str__(self):  # Возвращает размер и количество товара в нем в виде строки (например 42-1) цена и скидка
        return f'Размер: {self.size} - Кол-во: {self.quantity} - Цена: {self.price} - Скидака(%): {self.discount}'

    class Meta:
        verbose_name = 'Размер'  # Имя модели
        verbose_name_plural = 'Размеры'  # Имя модели во множественном числе
        db_table = 'size'  # Имя таблицы


# Модель цвета
class Color(models.Model):
    color = models.CharField(
        max_length=255,
        verbose_name='Color',
        help_text='Max 255 symbols, unique e.g. "Black"',
        unique=True,
    )  # Цвет

    def __str__(self):  # Возвращает цвет
        return self.color

    def save(self, *args, **kwargs):
        # API hex code to color name https://www.thecolorapi.com/docs
        # API
        url = f'https://www.thecolorapi.com/id?hex={self.color[1:]}'  # Получаем цвет по hex коду из базы данных (без #)
        # Получаем ответ от API
        response = requests.get(url)
        # Получаем JSON ответ от API
        json_response = response.json()
        # Получаем название цвета
        color_name = json_response['name']['value']
        # Перезаписываем цвет
        self.color = color_name
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Цвет'  # Имя модели
        verbose_name_plural = 'Цвета'  # Имя модели во множественном числе
        db_table = 'color'  # Имя таблицы


# Модель варианта продукта (товара) цвет, много размеров с количеством, цена и цена со скидкой в процентах, изображение
class ProductVariant(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name='Product',
        help_text='Product',
        related_name='product_variants',
    )  # Продукт
    name = models.CharField(
        max_length=255,
        verbose_name='Name',
        help_text='Nike Air Max 270 Red or Nike Air Max 270 Black',
    )  # Название
    color = models.ForeignKey(
        Color,
        on_delete=models.CASCADE,
        verbose_name='Color',
        help_text='Color',
        related_name='variants',
    )  # Цвет
    size = models.ManyToManyField(
        Size,
        verbose_name='Size',
        help_text='Size',
        related_name='variants_size',
    )  # Размер
    image = models.ImageField(
        upload_to='products/product_variant/',
        verbose_name='Image',
        help_text='Image',
    )  # Изображение

    def __str__(self):  # Возвращает цвет и размер
        # return f'{self.color} - {self.size}'
        return f'{self.color}  - {self.product}'  # Возвращает цвет, размер и продукт

    class Meta:
        verbose_name = 'Вариация продукта'  # Имя модели
        verbose_name_plural = 'Вариации продуктов'  # Имя модели во множественном числе
        db_table = 'product_variant'  # Имя таблицы


# Модель отзыва о продукте (товаре) с учетом пользователя
class Review(models.Model):
    user = models.ForeignKey(
        Account,
        on_delete=models.CASCADE,
        verbose_name='User',
        help_text='User',
    )  # Пользователь
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name='Product',
        help_text='Product',
    )  # Продукт
    text = models.TextField(
        verbose_name='Text',
        help_text='Text',
    )  # Текст
    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Created',
        help_text='Created',
    )  # Дата создания
    updated = models.DateTimeField(
        auto_now=True,
        verbose_name='Updated',
        help_text='Updated',
    )  # Дата обновления

    def __str__(self):  # Возвращает текст отзыва
        return self.text

    class Meta:
        verbose_name = 'Отзыв'  # Имя модели
        verbose_name_plural = 'Отзывы'  # Имя модели во множественном числе
        db_table = 'review'  # Имя таблицы
        ordering = ['-created']  # Сортировка по дате создания
