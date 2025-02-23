from django.core.files.storage import Storage
from django.conf import settings
import os

class CustomStorage(Storage):
    def _save(self, name, content):
        # Сохраняем файл в папку media/programs
        path = os.path.join(settings.MEDIA_ROOT, 'programs/pic/', name)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        try:
            with open(path, 'wb+') as destination:
                for chunk in content.chunks():
                    destination.write(chunk)
        except Exception as e:
            # Обработка ошибок (например, логирование)
            raise e
        return name

    def url(self, name):
        # Возвращаем URL файла
        return os.path.join(settings.MEDIA_URL, 'programs/pic/', name)

    def exists(self, name):
        # Проверяем, существует ли файл
        return os.path.exists(os.path.join(settings.MEDIA_ROOT, 'programs/pic/', name))