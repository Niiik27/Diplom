from django.apps import AppConfig

import APP_NAMES


class MessageConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = APP_NAMES.MESSAGE[APP_NAMES.NAME]
