from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class Account(AbstractBaseUser):
    """Менеджер учетных записей"""
    first_name = models.CharField(
        max_length=50,
        verbose_name='Имя',
        help_text='Максимальная длина 50 символов',
    )
    last_name = models.CharField(
        max_length=50,
        verbose_name='Фамилия',
        help_text='Максимальная длина 50 символов',
    )
    username = models.CharField(
        max_length=50,
        verbose_name='Имя пользователя',
        unique=True,
        help_text='Максимальная длина 50 символов и должна быть уникальной',
    )
    email = models.EmailField(
        max_length=320,
        verbose_name='Email',
        unique=True,
        help_text='Максимальная длина 320 символов и должна быть уникальной',
    )
    phone_number = models.CharField(
        max_length=20,
        verbose_name='Номер телефона',
        unique=True,
        help_text='Максимальная длина 30 символов и должна быть уникальной',
    )

    # required
    data_joined = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата и время создание аккаунта',
    )
    last_login = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата и время последнего входа'
    )
    is_admin = models.BooleanField(
        default=False,
        verbose_name='Администратор'
    )
    is_staff = models.BooleanField(
        default=False,
        verbose_name='Сотрудник'
    )
    is_active = models.BooleanField(
        default=False,
        verbose_name='Активый пользователь',
        help_text='Если не активый тогда будет как удаленый.'
    )
    is_superadmin = models.BooleanField(
        default=False,
        verbose_name='Супер администратор',
        help_text='Имя доступ ко всему'
    )
    # что бы авторизоваться по email адресу надо изменить поле `USERNAME_FIELD`
    USERNAME_FIELD = 'email'
    # обязательные поля
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    def __str__(self):
        return self.email

    # Права пользователя

    def has_perm(self, perm, obj=None):
        # Если пользователь является администратом тогда он(а) имеет все разрешения
        return self.is_admin
