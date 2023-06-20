from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name='Почта')

    phone = models.CharField(max_length=35, verbose_name='Номер телефона')
    avatar = models.ImageField(upload_to='users/', verbose_name='Аватар')
    country = models.CharField(max_length=100, verbose_name='Страна')
    token = models.CharField(max_length=100, verbose_name='Токен')

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []