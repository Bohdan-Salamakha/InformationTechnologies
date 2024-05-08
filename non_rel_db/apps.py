from django.apps import AppConfig


class NonRelDbConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'non_rel_db'
