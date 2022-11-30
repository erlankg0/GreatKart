from django.db import models
from django.urls import reverse

from category.utils import directory_path


class Category(models.Model):
    """Модель Категории"""
    name = models.CharField(
        max_length=50,
        verbose_name='Название категории',
        help_text='Название категории',
        unique=True
    )
    slug = models.SlugField(
        max_length=100,
        verbose_name='URL',
        help_text='URL',
        unique=True,
    )
    description = models.CharField(
        max_length=255,
        verbose_name='Описание категории',
        help_text='Описание категории'
    )
    image = models.ImageField(
        verbose_name='Изображение категории',
        help_text='Изображение категории',
        upload_to=directory_path,
        blank=True,
        null=True
    )

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('home', kwargs={"slug": self.slug})

    class Meta:
        db_table = 'category'
        ordering = ['-name']
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
