from typing import List

from django.contrib.auth.models import AbstractUser
from django.db import models

from .managers import CustomUserManager

NULLABLE = {'blank': True, 'null': True}


class CustomUser(AbstractUser):
    """
    Модель, описывающая пользователя.
    Наследуется от AbstractUser.
    """
    objects = CustomUserManager()

    username = None
    email = models.EmailField(unique=True, verbose_name='Электронная почта', max_length=254)
    first_name = models.CharField(max_length=64, verbose_name="Имя")
    last_name = models.CharField(max_length=64, verbose_name="Фамилия")

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        db_table = 'users'

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    @classmethod
    def get_all_users(cls) -> List['CustomUser']:
        """
        Возвращает список всех пользователей
        """
        return cls.objects.all()
