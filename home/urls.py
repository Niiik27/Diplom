from django.urls import path
from .views import HomeTempateView

urlpatterns = [
    path('', HomeTempateView.as_view(), name='home'),
]
