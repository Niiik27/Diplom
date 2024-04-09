
from django.urls import path
from . import views


urlpatterns = [
    path('', views.portfolioView, name=views.app_name),
]
