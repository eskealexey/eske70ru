from accounts.models import CustomUser
from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from tinymce.models import HTMLField
from django.db import models
from django.utils import timezone

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

    @property
    def active_comments(self):
        return self.comments.filter(is_active=True)


User = get_user_model()

class Comment(models.Model):
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Проект'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор'
    )
    text = models.TextField('Текст комментария', max_length=1000)
    created_at = models.DateTimeField('Дата создания', default=timezone.now)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)
    is_active = models.BooleanField('Активен', default=True)
    parent = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='replies',
        verbose_name='Родительский комментарий'
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['-created_at']  # Сортировка по дате создания

    def __str__(self):
        return f'Комментарий от {self.author} к проекту {self.project}'

    def get_absolute_url(self):
        return reverse('project_detail', kwargs={'slug': self.project.slug}) + f'#comment-{self.id}'

    @property
    def is_reply(self):
        """Проверяет, является ли комментарий ответом"""
        return self.parent is not None

    @property
    def get_replies(self):
        """Возвращает все ответы на этот комментарий"""
        return self.replies.filter(is_active=True).order_by('created_at')