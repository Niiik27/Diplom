from django.urls import path

from . import views
import APP_NAMES

urlpatterns = [
path('', views.CreateTeamView.as_view(), name=APP_NAMES.TEAMS[APP_NAMES.NAME]),
path(APP_NAMES.TEAM_CREATE[APP_NAMES.NAME], views.CreateTeamView.as_view(), name=APP_NAMES.TEAM_CREATE[APP_NAMES.NAME]),
path(APP_NAMES.TEAM_LIST[APP_NAMES.NAME], views.TeamsView.as_view(), name=APP_NAMES.TEAM_LIST[APP_NAMES.NAME]),
path(f'{APP_NAMES.JOIN_TEAM[APP_NAMES.NAME]}/<str:username>/', views.JoinTeamView.as_view(),name=APP_NAMES.JOIN_TEAM[APP_NAMES.NAME]),
path(f'{APP_NAMES.TEAM_VIEW[APP_NAMES.NAME]}/<str:username>/', views.TeamView.as_view(),name=APP_NAMES.TEAM_VIEW[APP_NAMES.NAME]),
]

