from django.urls import path, re_path

from .consumers import EmailConsumer

ws_urlpatterns = [
    # path('ws/emails/<int:email_account_id>/', EmailConsumer.as_asgi()),
    re_path(r'ws/emails/(?P<email_account_id>\d+)/$', EmailConsumer.as_asgi())
]