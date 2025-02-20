from django.db import models
from tinymce import models as tinymce_models

# Create your models here.
class Platforms(models.Model):
    """Модель платформ"""
    name = models.CharField(max_length=200, verbose_name='Название')

    def __str__(self):
        return self.name


class Languages(models.Model):
    """Модель языков программирования"""
    name = models.CharField(max_length=200, verbose_name='Название')
    def __str__(self):
        return self.name


class Program(models.Model):
    """Модель программы"""
    name = models.CharField(max_length=200, verbose_name='Название')
    short_description = models.CharField(max_length=200, verbose_name='Краткое описание')
    platforms = models.ForeignKey(Platforms, on_delete=models.CASCADE, verbose_name='Платформа')
    languages = models.ForeignKey(Languages, on_delete=models.CASCADE, verbose_name='Язык программирования')
    description = tinymce_models.HTMLField(blank=True, verbose_name='Описание')
    image = models.ImageField(upload_to='programs/img/', verbose_name='Изображение')
    file = models.FileField(upload_to='programs/files/', verbose_name='Файл')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Программа'
        verbose_name_plural = 'Программы'
        ordering = ['name']

