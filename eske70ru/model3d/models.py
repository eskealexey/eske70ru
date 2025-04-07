from django.contrib.auth import get_user_model
from django.db import models

# Create your models hfrom django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils.text import slugify

User = get_user_model()

class Category(models.Model):
    """Категории для 3D моделей"""
    name = models.CharField('Название', max_length=100)
    slug = models.SlugField('URL', max_length=100, unique=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Tag(models.Model):
    """Теги для 3D моделей"""
    name = models.CharField('Название', max_length=50, unique=True)
    slug = models.SlugField('URL', max_length=50, unique=True)

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Model3D(models.Model):
    """3D модель с описанием и файлами"""
    FORMAT_CHOICES = [
        ('stl', 'STL'),
        ('obj', 'OBJ'),
        ('fbx', 'FBX'),
        ('blend', 'Blender'),
        ('other', 'Другое'),
    ]

    STATUS_CHOICES = [
        ('draft', 'Черновик'),
        ('published', 'Опубликовано'),
        ('archived', 'В архиве'),
    ]

    title = models.CharField('Название модели', max_length=200)
    slug = models.SlugField('URL', max_length=200, unique=True)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='models3d',
        verbose_name='Автор'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Категория'
    )
    tags = models.ManyToManyField(
        Tag,
        blank=True,
        verbose_name='Теги'
    )
    description = models.TextField('Описание модели')
    model_file = models.FileField(
        'Файл 3D модели',
        upload_to='3d_models/files/',
        help_text='Загрузите файл 3D модели'
    )
    format = models.CharField(
        'Формат файла',
        max_length=10,
        choices=FORMAT_CHOICES,
        default='stl'
    )
    preview_image = models.ImageField(
        'Превью модели',
        upload_to='3d_models/previews/',
        help_text='Основное изображение для превью'
    )
    license = models.CharField(
        'Лицензия',
        max_length=100,
        blank=True,
        default='Creative Commons'
    )
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)
    status = models.CharField(
        'Статус',
        max_length=10,
        choices=STATUS_CHOICES,
        default='draft'
    )
    download_count = models.PositiveIntegerField('Количество скачиваний', default=0)
    # poly_count = models.PositiveIntegerField('Количество полигонов', default=0)
    # is_animated = models.BooleanField('Анимированная модель', default=False)
    # is_rigged = models.BooleanField('Ригged модель', default=False)
    # is_printable = models.BooleanField('Готова для 3D печати', default=False)

    class Meta:
        verbose_name = '3D модель'
        verbose_name_plural = '3D модели'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['status']),
        ]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('model3d_detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class ModelImage(models.Model):
    """Дополнительные изображения для 3D модели"""
    model = models.ForeignKey(
        Model3D,
        on_delete=models.CASCADE,
        related_name='images',
        verbose_name='3D модель'
    )
    image = models.ImageField(
        'Изображение',
        upload_to='3d_models/images/',
        help_text='Дополнительные изображения модели'
    )
    description = models.CharField(
        'Описание изображения',
        max_length=200,
        blank=True
    )
    is_main = models.BooleanField(
        'Основное изображение',
        default=False,
        help_text='Если отмечено, заменит основное превью'
    )
    created_at = models.DateTimeField('Дата добавления', auto_now_add=True)

    class Meta:
        verbose_name = 'Изображение модели'
        verbose_name_plural = 'Изображения моделей'
        ordering = ['-is_main', 'created_at']

    def __str__(self):
        return f"Изображение для {self.model.title}"

    def save(self, *args, **kwargs):
        if self.is_main:
            # Снимаем флаг is_main у других изображений этой модели
            ModelImage.objects.filter(model=self.model).exclude(pk=self.pk).update(is_main=False)
            # Обновляем основное превью модели
            self.model.preview_image = self.image
            self.model.save()
        super().save(*args, **kwargs)