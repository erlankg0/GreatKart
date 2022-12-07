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
    )
    # нужно сделать валлидацию номера телефона
    phone = models.CharField(
        verbose_name='Номер телефона',
        unique=True,
        blank=True,
        null=True,
        max_length=50
    )
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'phone']

    def __str__(self):
        return self.email
