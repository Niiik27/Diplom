from django.urls import path

from . import views
import APP_NAMES

urlpatterns = [
path('', views.CreateTeamView.as_view(), name=APP_NAMES.TEAM[APP_NAMES.NAME]),
# path('APP_NAMES.TEAM_CREATE[APP_NAMES.NAME]', views.CreateTeamView.as_view(), name=APP_NAMES.TEAM_CREATE[APP_NAMES.NAME]),
]

