import re

from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, AbstractUser


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


class CustomUserManager(BaseUserManager):
    """
    Creates and saves a User with the given email, date of
    birth and password.
    """

    # создание пользователя
    def create_user(self, username, email, phone, password=None) -> None:
        if not email:
            raise ValueError("У пользователя должная быть email")
        if not username:
            raise ValueError("У пользователя должная быть username")
        if not phone:
            raise ValueError("У пользователя должен быть номер телефона")

        user = self.model(
            email=self.normalize_email(email),  # нормализация email
            username=username,
            phone=phone
        )
        user.set_password(password)  # сохранения пароля
        user.save(using=self._db)  # сохранения пользователя
        return user

    def create_superuser(self, username, email, phone, password):
        user = self.create_user(
            email=email,
            username=username,
            phone=phone,
            password=password
        )
        user.is_staff = True
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class Account(AbstractUser):
    # only add email field for login

    email = models.EmailField(
        verbose_name='Email',
        max_length=50,
        unique=True
    )  # email
    # нужно сделать валлидацию номера телефона
    phone = models.CharField(
        verbose_name='Номер телефона',
        unique=True,
        blank=True,
        null=True,
        max_length=50
    )  # номер телефона

    is_active = models.BooleanField(default=True)  # активный пользователь
    is_admin = models.BooleanField(default=False)  # администратор

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'  # логин по email
    REQUIRED_FIELDS = ['username', 'phone']  # Email & Password are required by default.

    def __str__(self):
        return self.email  # возвращает email

    # проверка номера телефона на корректность regex
    def clean_phone(self):
        phone = self.cleaned_data['phone']  # получение номера телефона
        if 10 <= len(phone) <= 15:  # проверка длины номера телефона от 10 до 15 символов
            if re.match(r'^(\+\d{1,2}\s)?\(?\d{3}\)?[\s.-]\d{3}[\s.-]\d{4}$',
                        phone):
                """
                проверка на корректность номера телефона по регулярному выражению regex (пример +7 (999) 999-9999) 
                или (999) 999-9999 или 999-999-9999 или 999.999.9999 или 999 999 9999
                """

                return phone  # возвращает номер телефона
            else:
                raise ValidationError("Номер телефона не корректен")  # исключение валидации номера телефона


class Address(models.Model):
    user = models.OneToOneField(
        Account,
        on_delete=models.CASCADE,
        related_name='address_user',
        verbose_name='Адрес пользователя'
    )  # связь с моделью пользователя
    country = models.CharField(
        verbose_name='Страна',
        max_length=50
    )  # страна
    city = models.CharField(
        verbose_name='Город',
        max_length=50
    )  # город
    street = models.CharField(
        verbose_name='Улица',
        max_length=50
    )  # улица
    house = models.CharField(
        verbose_name='Дом',
        max_length=50
    )  # дом
    apartment = models.CharField(
        verbose_name='Квартира',
        max_length=50,
        blank=True,
        null=True
    )  # квартира

    def __str__(self):
        return f'{self.country}, {self.city}, {self.street}, {self.house}, {self.apartment}'

    def get_user(self):
        return self.user

    class Meta:
        verbose_name = 'Адрес'
        verbose_name_plural = 'Адреса'
        db_table = 'address'
