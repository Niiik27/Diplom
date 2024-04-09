from django.contrib.auth.views import LogoutView
from django.urls import path, include

from django.contrib.auth import logout
from django.shortcuts import redirect
from . import views
import APP_NAMES
from .views import ProfileView

def my_logout_view(request):
    logout(request)
    return redirect('home')
urlpatterns = [
    path('', views.UserLoginView.as_view(), name = APP_NAMES.LOGIN[APP_NAMES.NAME]),
    path(f'{APP_NAMES.REGISTER[APP_NAMES.NAME]}/', views.UserCreateView.as_view(), name = APP_NAMES.REGISTER[APP_NAMES.NAME]),
    path(f'{APP_NAMES.LOGOUT[APP_NAMES.NAME]}/', my_logout_view, name=APP_NAMES.LOGOUT[APP_NAMES.NAME]),
    path(f'{APP_NAMES.USERS[APP_NAMES.NAME]}/', views.CustomUserListView.as_view(),
         name=APP_NAMES.USERS[APP_NAMES.NAME]),

    path('<str:username>/', views.ProfileView.as_view(), name=APP_NAMES.PROFILE[APP_NAMES.NAME]),
    path(f'<str:username>/{APP_NAMES.EDIT[APP_NAMES.NAME]}/', views.UserUpdateView.as_view(), name=APP_NAMES.EDIT[APP_NAMES.NAME]),

]

