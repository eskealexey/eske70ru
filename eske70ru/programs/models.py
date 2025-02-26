from django.db import models

from django_ckeditor_5.fields import CKEditor5Field


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
    objects = None
    name = models.CharField(max_length=200, verbose_name='Название')
    short_description = models.CharField(max_length=200, verbose_name='Краткое описание')
    platforms = models.ForeignKey(Platforms, on_delete=models.CASCADE, verbose_name='Платформа')
    languages = models.ForeignKey(Languages, on_delete=models.CASCADE, verbose_name='Язык программирования')
    description = CKEditor5Field('Text', config_name='extends')
    image = models.ImageField(upload_to='programs/img/',  verbose_name='Изображение')
    file = models.FileField(upload_to='programs/files/', verbose_name='Файл')
    date = models.DateField(auto_now_add=False, verbose_name='Дата добавления', null=True)
    is_active = models.BooleanField(default=False, verbose_name='Активна')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Программа'
        verbose_name_plural = 'Программы'
        ordering = ['name']


class SoftDownload(models.Model):
    """Модель скачивания программ"""
    objects = None
    program_id = models.IntegerField(verbose_name='ID программы')
    ip_remote = models.CharField(verbose_name='IP адрес', max_length=15, null=True)
    date = models.DateTimeField(auto_now_add=True, verbose_name='Дата скачивания', null=True, blank=True)
    count = models.IntegerField(verbose_name='Количество скачиваний', default=1)

    def __str__(self):
        return self.ip_remote