from django.apps import AppConfig


class ExtendedAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'extended_app'
