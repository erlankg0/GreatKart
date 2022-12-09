from django.db import models
from django.urls import reverse
from django.utils.safestring import mark_safe
from mptt.models import TreeForeignKey, MPTTModel

from store.utils import directory_image_path, get_sizes
from accounts.models import Account
# for get color_name (use other API )
import requests

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


class Images(models.Model):
    name = models.CharField(
        verbose_name='Название картинки',
        max_length=155,
    )
    image = models.ImageField(
        upload_to='images/',
        verbose_name='Картинка'
    )
    product = models.ForeignKey(
        'Product',
        on_delete=models.CASCADE,
        verbose_name='Картинка для продукта'

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

    def count(self) -> int:
        return self.count()

    class Meta:
        verbose_name = 'Нравится'
        verbose_name_plural = 'Нравится'
        db_table = 'like'  # Имя таблицы


class Size(models.Model):
    """Размер продукта"""
    size = models.CharField(
        max_length=10,
        verbose_name='Размер/объем'
    )

    def __str__(self):
        return self.size

    class Meta:
        verbose_name = 'Размер'
        verbose_name_plural = 'Размеры'
        db_table = 'size'  # Имя таблицы


class Color(models.Model):
    """Таблица для хранения цветов товаров"""
    name = models.CharField(
        max_length=100,
        verbose_name='Название цвета',
        blank=True,
        null=True
    )
    color = models.CharField(
        max_length=50,
        verbose_name='Цвет товара',
    )

    def save(self, *args, **kwargs):
        rq = requests.get(f"https://www.thecolorapi.com/id?hex={self.color[1:]}").json()['name']['value']
        self.name = rq
        return super(Color, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

    def color_tag(self):
        if self.color is not None:
            return mark_safe('<p style="background-color:{}">Цвет</p>'.format(self.color))
        return '-'

    class Meta:
        verbose_name = 'Цвет товар'
        verbose_name_plural = 'Цвета товаров'
        db_table = 'color'  # Имя таблицы


#
# class Quantity(models.Model):
#     """Таблица для хранения колличество товаров"""
#     quantity = models.PositiveIntegerField(
#         verbose_name='Колличество товара'
#     )
#
#     def __str__(self):
#         return str(self.quantity)
#
#     class Meta:
#         verbose_name = 'Колличество товара'
#         verbose_name_plural = 'Колличество товаров'
#         db_table = 'quantity'  # Имя таблицы


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

    def get_absolute_url(self):
        return reverse('shot_by_brand', kwargs={"slug": self.slug})

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
        # on_delete=models.PROTECT,  # Категория не удалится пока не будет удалено товар(продукт),
        verbose_name='Категория товара'
    )  # many to one relation with Category
    keywords = models.CharField(
        verbose_name='Ключевые слова',
        max_length=255,
    )
    image = models.ImageField(
        upload_to=directory_image_path,
        verbose_name='Изображение товара(продукта)'
    )
    sold = models.PositiveIntegerField(
        verbose_name='Продано',
        blank=True,
        default=0
    )
    is_available = models.BooleanField(
        default=False,
        verbose_name='В продаже',
        help_text='В продаже, если в складе не осталось будет убрана с продажи',
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
        unique=True,
        verbose_name='URL'
    )
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    # method to create a fake table field in read only mode
    def image_tag(self):
        if self.image.url is not None:
            return mark_safe('<img src="{}" height="50"/>'.format(self.image.url))
        else:
            return ""

    def category_name(self):
        self.name = Product.category.name
        return self.name

    def get_absolute_url(self):
        return reverse('detail_product', args=[self.slug])

    def liked_count(self) -> int:  # Count total like
        return len(Like.objects.filter(user__like__product=self))

    class Meta:
        ordering = ['-name', ]
        db_table = 'products'  # Имя таблицы
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'


class Variants(models.Model):
    name = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name='Название варианта',
        help_text='Пример T-Shirt размер S'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name='Связь с продуктом',
        related_name='variant_product',
    )
    image = models.ForeignKey(
        Images,
        on_delete=models.CASCADE,
        verbose_name='Изображение'
    )
    price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
        verbose_name='Цена товара без скидок'
    )
    discount_price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=1,
        verbose_name='Скидочная цена'
    )
    color = models.ForeignKey(
        Color,
        on_delete=models.CASCADE,
        verbose_name='Цвет продукта',
        blank=True,
        null=True,
    )
    size = models.ForeignKey(
        Size,
        on_delete=models.CASCADE,
        verbose_name='Размер продукта',
        blank=True,
        null=True,
    )
    quantity = models.PositiveIntegerField(
        default=0,
        verbose_name='Количество товара'
    )

    slug = models.SlugField(
        unique=True,
        verbose_name='URL варианта'
    )

    def __str__(self):
        return self.name

    def image_tag(self):
        img = Images.objects.get(id=self.image_id)
        if img.id is not None:
            return mark_safe(f'<img src="{img.image_.url}" height="50"/>')
        else:
            return ''

    def image_(self):
        img = Images.objects.get(image=self.image)
        if img is not None:
            var_image = img.image.url
        else:
            var_image = ''
        return var_image
