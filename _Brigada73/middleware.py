# middleware.py

from channels.middleware import BaseMiddleware
from channels.db import database_sync_to_async
# from django.contrib.auth.models import AnonymousUser
# from rest_framework_simplejwt.tokens import AccessToken
from django.contrib.auth import get_user_model

class TokenAuthMiddleware(BaseMiddleware):
    def __init__(self, inner):
        super().__init__(inner)

    async def __call__(self, scope, receive, send):
        headers = dict(scope['headers'])
        if b'authorization' in headers:
            try:
                token_name, token_key = headers[b'authorization'].decode().split()
                if token_name.lower() == 'bearer':
                    user = await self.get_user(token_key)
                    scope['user'] = user
            except Exception as e:
                print(e)
        return await super().__call__(scope, receive, send)

    @database_sync_to_async
    def get_user(self, token_key):
        try:
            # token = AccessToken(token_key)
            # user = get_user_model().objects.get(id=token['user_id'])
            return user
        except:
            return None
