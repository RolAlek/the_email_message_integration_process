import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from emails.routing import ws_urlpatterns

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE", "the_message_integration_project.settings"
)

application =  ProtocolTypeRouter({
    'http': get_asgi_application(),
    'websocket': AuthMiddlewareStack(
        URLRouter(ws_urlpatterns)
    )
})
