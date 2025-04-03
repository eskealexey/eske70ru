from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True, verbose_name='Электронная почта')
    is_verified = models.BooleanField(default=False, verbose_name='Подтвержден')
    gender = models.CharField(max_length=10, default='мужской', choices=(('male', 'мужской'), ('female', 'женский')), verbose_name='Пол')
    birthday = models.DateField(null=True, blank=True, verbose_name='Дата рождения')
    country = models.CharField(max_length=100, null=True, blank=True, verbose_name='Страна')
    city = models.CharField(max_length=100, null=True, blank=True, verbose_name='Город')
