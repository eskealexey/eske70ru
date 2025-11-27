from django.apps import AppConfig


class ProjectsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'projects'



class YourAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'projects'  # замените на имя вашего приложения

    def ready(self):
        # Импортируем сигналы для их регистрации
        import eske70ru.projects.signals