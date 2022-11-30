from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


# Менеджер аккаунтов
class AccountManager(BaseUserManager):
    # создание пользователя
    def create_user(self, first_name, last_name, username, email, password=None) -> None:
        if not email:
            raise ValueError("У пользователя должная быть email")

        if not username:
            raise ValueError("У пользователя должная быть username")
        user = self.model(
            email=self.normalize_email(email),  # нормализация email
            username=username,
            first_name=first_name,
            last_name=last_name,
        )
        user.set_password(password)  # сохранения пароля
        user.save(using=self._db)  # сохранения пользователя
        return user

    # создание супер пользователя
    def create_superuser(self, first_name, last_name, username, email, password):
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name
        )
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True
        user.save(using=self._db)
        return user


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
    objects = AccountManager()  # изменить менеджер

    # required
    date_joined = models.DateTimeField(
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
        default=True,
        verbose_name='Активый пользователь',
        help_text='Если не активый тогда будет как удаленый.'
    )
    is_superadmin = models.BooleanField(
        default=False,
        verbose_name='Супер администратор',
        help_text='Имеет доступ ко всему'
    )
    # что бы авторизоваться по email адресу надо изменить поле `USERNAME_FIELD`
    USERNAME_FIELD = 'email'
    # обязательные поля
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        if self.is_admin or self.is_superadmin:
            self.is_staff = True
        if self.is_superadmin:
            self.is_admin = True
        self.is_active = True
        super(Account, self).save(*args, **kwargs)

    # Права пользователя

    def has_perm(self, perm, obj=None):
        # Если пользователь является администратом тогда он(а) имеет все разрешения
        return self.is_admin

    def has_module_perms(self, add_label):
        return True
