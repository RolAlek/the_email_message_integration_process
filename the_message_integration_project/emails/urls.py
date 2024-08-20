from django.urls import path

from .views import EmailAccountCreateView, EmailMessagesView

app_name = 'emails'

urlpatterns = [
    path('', EmailAccountCreateView.as_view(), name='add_email'),
    path(
        'messages/',
        EmailMessagesView.as_view(),
        name='messages',
    ),
]
