from django.urls import path, include

from django.contrib.auth import logout
from django.shortcuts import redirect
from . import views
import APP_NAMES

def my_logout_view(request):
    logout(request)
    return redirect('home')
urlpatterns = [
    path('', views.OrderListView.as_view(), name=APP_NAMES.ORDERS[APP_NAMES.NAME]),
    path(f'{APP_NAMES.TAKE_ORDER[APP_NAMES.NAME]}/<str:customer>/', views.TakeOrderView.as_view(), name=APP_NAMES.TAKE_ORDER[APP_NAMES.NAME]),
]

