from django.contrib.auth.models import AbstractUser, Group
from django.db import models


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name='Почта')

    phone = models.CharField(max_length=35, verbose_name='Номер телефона')
    avatar = models.ImageField(upload_to='users/', verbose_name='Аватар')
    country = models.CharField(max_length=100, verbose_name='Страна')
    token = models.CharField(max_length=100, verbose_name='Токен')
    is_moderator = models.BooleanField(default=False, verbose_name='Модератор')

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def save(self, *args, **kwargs):
        # Проверка, если пользователь является модератором, добавляем его в группу "Модераторы"
        if self.is_moderator and not self.groups.filter(name='Модераторы').exists():
            group = Group.objects.get(name='Модераторы')
            self.groups.add(group)
        super().save(*args, **kwargs)
