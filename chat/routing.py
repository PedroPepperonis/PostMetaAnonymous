from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<room_name>\w+)/$', consumers.ChatConsumer.as_asgi()),
]

#The next step is to point the root routing configuration at the chat.routing module.
# In mysite/asgi.py, import AuthMiddlewareStack, URLRouter, and chat.routing; and insert a 'websocket' key in the
# ProtocolTypeRouter list in the following format: