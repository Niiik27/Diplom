from django.apps import AppConfig
import APP_NAMES


class CustomUserConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = APP_NAMES.PROFILE[APP_NAMES.NAME]
    verbose_name = APP_NAMES.PROFILE[APP_NAMES.VERBOSE]
