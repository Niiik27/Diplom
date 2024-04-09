import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import _Brigada73.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', '_Brigada73.settings')
application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            _Brigada73.routing.websocket_urlpatterns  # Маршруты WebSocket
        )
    ),
})
