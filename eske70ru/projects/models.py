from django.db import models
from django.contrib.auth.models import User
from tinymce.models import HTMLField

from accounts.models import CustomUser


class Project(models.Model):
    CATEGORY_CHOICES = [
        ('power', 'Силовые установки'),
        ('lighting', 'Освещение'),
        ('automation', 'Автоматизация'),
        ('control', 'Системы управления'),
        ('other', 'Другое'),
    ]

    STATUS_CHOICES = [
        ('draft', 'Черновик'),
        ('published', 'Опубликовано'),
        ('archived', 'В архиве'),
    ]

    title = models.CharField('Название проекта', max_length=200)
    slug = models.SlugField('URL', max_length=200, unique=True)
    author = models.ForeignKey( CustomUser, on_delete=models.CASCADE, related_name='projects')
    category = models.CharField('Категория', max_length=20, choices=CATEGORY_CHOICES)
    description = HTMLField('Описание проекта')
    short_description = models.TextField('Краткое описание', max_length=300)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)
    status = models.CharField('Статус', max_length=10, choices=STATUS_CHOICES, default='draft')
    views = models.PositiveIntegerField('Просмотры', default=0)
    rating = models.FloatField('Рейтинг', default=0)
    image = models.ImageField('Изображение', upload_to='project_images/', blank=True, null=True)
    # difficulty = models.PositiveSmallIntegerField('Сложность (1-5)', default=3)

    class Meta:
        verbose_name = 'Проект'
        verbose_name_plural = 'Проекты'
        ordering = ['-created_at']

    def __str__(self):
        return self.title