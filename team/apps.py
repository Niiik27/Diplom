from django.apps import AppConfig
import APP_NAMES

class OrdersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = APP_NAMES.TEAM[APP_NAMES.NAME]
