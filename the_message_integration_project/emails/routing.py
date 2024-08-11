from django.urls import path

from .consumers import EmailConsumer

ws_urlpatterns = [
    path('ws/emails/', EmailConsumer.as_asgi()),
]