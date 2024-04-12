from django.urls import path, re_path
from . import consumers

websocket_urlpatterns = [
    path('ws/chat/', consumers.ChatConsumer.as_asgi()),
    path('ws/history/', consumers.HistoryConsumer.as_asgi()),
    path('ws/notify/', consumers.NotifyConsumer.as_asgi()),
]
