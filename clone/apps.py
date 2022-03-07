from django.apps import AppConfig


class CloneConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'clone'
# add this
    def ready(self):
        import clone.signals 