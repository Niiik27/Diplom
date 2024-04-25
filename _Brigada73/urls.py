"""
URL configuration for _Brigada73 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

import APP_NAMES

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(f'{APP_NAMES.HOME[APP_NAMES.NAME]}.urls')),
    path(f'{APP_NAMES.PROFILE[APP_NAMES.NAME]}/', include(f'{APP_NAMES.PROFILE[APP_NAMES.NAME]}.urls')),
    path(f'{APP_NAMES.ORDERS[APP_NAMES.NAME]}/', include(f'{APP_NAMES.ORDERS[APP_NAMES.NAME]}.urls')),

    path('<str:username>/', include(f'{APP_NAMES.HOME[APP_NAMES.NAME]}.urls')),

    path(f'<str:username>/{APP_NAMES.PORTFOLIO[APP_NAMES.NAME]}', include(f'{APP_NAMES.PORTFOLIO[APP_NAMES.NAME]}.urls')),
    path(f'<str:username>/{APP_NAMES.TEAM[APP_NAMES.NAME]}',include(f'{APP_NAMES.TEAM[APP_NAMES.NAME]}.urls')),

    path(f'<str:username>/{APP_NAMES.MESSAGE[APP_NAMES.NAME]}/<str:recipient>',include(f'{APP_NAMES.MESSAGE[APP_NAMES.NAME]}.urls')),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
