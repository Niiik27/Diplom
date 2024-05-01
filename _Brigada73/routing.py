from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path
from . import consumers
from .middleware import TokenAuthMiddleware

websocket_urlpatterns = [
    path('ws/chat/', consumers.ChatConsumer.as_asgi()),
    path('ws/notify/', consumers.NotifyConsumer.as_asgi()),
]
# application = ProtocolTypeRouter({
#     'websocket': AuthMiddlewareStack(
#         TokenAuthMiddleware(
#             URLRouter(
#                 websocket_urlpatterns
#             )
#         )
#     ),
# })
