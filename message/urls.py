from django.urls import path, include
from . import views
import APP_NAMES



urlpatterns = [
    path('', views.MessageView.as_view(), name=APP_NAMES.MESSAGE[APP_NAMES.NAME]),
]
