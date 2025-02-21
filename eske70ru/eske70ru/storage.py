from django.core.files.storage import FileSystemStorage

class CustomStorage(FileSystemStorage):
    def get_available_name(self, name, max_length=None):
        # Здесь вы можете переопределить логику получения имени файла
        return super().get_available_name(name, max_length)