import os

from accounts.models import CustomUser
from django.contrib.auth import get_user_model
from django.core.files.storage import default_storage
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

        # ... существующие поля ...

    @property
    def active_files(self):
        """Активные файлы проекта"""
        return self.files.filter(is_active=True)

    @property
    def files_count(self):
        """Количество файлов проекта"""
        return self.active_files.count()

    @property
    def total_files_size(self):
        """Общий размер всех файлов проекта"""
        return self.active_files.aggregate(total_size=models.Sum('size'))['total_size'] or 0

    def get_files_by_type(self):
        """Группировка файлов по типам"""
        return {
            file_type: self.active_files.filter(file_type=file_type)
            for file_type, _ in ProjectFile.FILE_TYPES
        }

    def get_supported_file_types(self):
        """Возвращает список типов файлов, присутствующих в проекте"""
        return self.active_files.values_list('file_type', flat=True).distinct()


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


def project_files_path(instance, filename):
    """Генерирует путь для файлов проекта"""
    return f'projects/{instance.project.slug}/files/{filename}'


class ProjectFile(models.Model):
    FILE_TYPES = [
        ('document', 'Документ'),
        ('scheme', 'Схема'),
        ('code', 'Исходный код'),
        ('firmware', 'Прошивка'),
        ('model', '3D-модель'),
        ('image', 'Изображение'),
        ('other', 'Другое'),
    ]

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='files',
        verbose_name='Проект'
    )
    file = models.FileField(
        'Файл',
        upload_to=project_files_path,
        max_length=500
    )
    name = models.CharField('Название файла', max_length=200)
    file_type = models.CharField(
        'Тип файла',
        max_length=20,
        choices=FILE_TYPES,
        default='document'
    )
    description = models.TextField('Описание файла', blank=True, max_length=500)
    uploaded_at = models.DateTimeField('Дата загрузки', auto_now_add=True)
    size = models.PositiveIntegerField('Размер файла (байт)', default=0)
    download_count = models.PositiveIntegerField('Количество скачиваний', default=0)
    is_active = models.BooleanField('Активный', default=True)

    class Meta:
        verbose_name = 'Файл проекта'
        verbose_name_plural = 'Файлы проектов'
        ordering = ['file_type', 'uploaded_at']

    def __str__(self):
        return f"{self.name} ({self.project.title})"

    def save(self, *args, **kwargs):
        # Автоматически определяем размер файла при сохранении
        if self.file and not self.size:
            self.size = self.file.size
        # Если имя не указано, используем оригинальное имя файла
        if not self.name and self.file:
            self.name = os.path.basename(self.file.name)
        super().save(*args, **kwargs)

    def get_file_extension(self):
        """Возвращает расширение файла"""
        if self.file:
            return os.path.splitext(self.file.name)[1].lower()
        return ''

    def get_file_size_display(self):
        """Возвращает размер файла в удобном формате"""
        if self.size < 1024:
            return f"{self.size} Б"
        elif self.size < 1024 * 1024:
            return f"{self.size / 1024:.1f} КБ"
        elif self.size < 1024 * 1024 * 1024:
            return f"{self.size / (1024 * 1024):.1f} МБ"
        else:
            return f"{self.size / (1024 * 1024 * 1024):.1f} ГБ"

    def increment_download_count(self):
        """Увеличивает счетчик скачиваний"""
        self.download_count += 1
        self.save(update_fields=['download_count'])
