"""
ASGI config for multiserver project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""

# import os

# from django.core.asgi import get_asgi_application

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'multiserver.settings')

# application = get_asgi_application()
import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from services import consumers
from django.urls import path

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'multiserver.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter([
            path('ws/chat/', consumers.ChatConsumer.as_asgi()),
        ])
    ),
})