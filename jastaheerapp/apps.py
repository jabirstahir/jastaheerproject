from django.apps import AppConfig


class JastaheerappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'jastaheerapp'

    def ready(self):
        import jastaheerapp.signals # replace with your app's actual name