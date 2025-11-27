from django.db.models.signals import pre_delete, post_save, pre_save
from django.dispatch import receiver
from django.core.files.storage import default_storage
import os
from .models import ProjectFile


@receiver(pre_delete, sender=ProjectFile)
def delete_project_file(sender, instance, **kwargs):
    """
    Удаляет физический файл из файловой системы при удалении записи ProjectFile
    """
    if instance.file:
        # Используем default_storage для корректного удаления файлов
        # Это работает с любым бэкендом хранения (локальным, S3 и т.д.)
        if default_storage.exists(instance.file.name):
            default_storage.delete(instance.file.name)


@receiver(pre_save, sender=ProjectFile)
def auto_set_file_info(sender, instance, **kwargs):
    """
    Автоматически устанавливает размер файла и имя при сохранении
    """
    if instance.file and not instance.pk:  # Только для новых файлов
        # Устанавливаем размер файла
        instance.size = instance.file.size

        # Если имя не указано, используем оригинальное имя файла
        if not instance.name:
            # Убираем расширение для красивого отображения
            original_name = os.path.basename(instance.file.name)
            name_without_ext = os.path.splitext(original_name)[0]
            instance.name = name_without_ext


# В signals.py
from django.db.models.signals import post_delete
from django.dispatch import receiver
from .models import Project, ProjectFile


@receiver(post_delete, sender=ProjectFile)
def cleanup_empty_directories(sender, instance, **kwargs):
    """
    Очищает пустые директории после удаления файлов
    """
    if instance.file:
        file_path = instance.file.name
        directory = os.path.dirname(file_path)

        # Проверяем, пуста ли директория (упрощенная версия)
        try:
            # Для локального хранилища
            if default_storage.exists(directory) and not default_storage.listdir(directory)[1]:
                default_storage.delete(directory)
        except:
            # Игнорируем ошибки при удалении директорий
            pass


@receiver(pre_save, sender=ProjectFile)
def update_file_on_change(sender, instance, **kwargs):
    """
    Обрабатывает изменение файла (удаляет старый файл при загрузке нового)
    """
    if instance.pk:
        try:
            old_instance = ProjectFile.objects.get(pk=instance.pk)
            if old_instance.file and old_instance.file != instance.file:
                # Удаляем старый файл
                if default_storage.exists(old_instance.file.name):
                    default_storage.delete(old_instance.file.name)
        except ProjectFile.DoesNotExist:
            pass