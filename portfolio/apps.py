from django.apps import AppConfig
import APP_NAMES



class PortfolioConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = APP_NAMES.PORTFOLIO[APP_NAMES.NAME]
    verbose_name = APP_NAMES.PORTFOLIO[APP_NAMES.VERBOSE]
