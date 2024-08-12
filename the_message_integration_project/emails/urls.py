from django.urls import path

from .views import EmailAccountCreateView, EmailMessagesView

app_name = 'emails'

urlpatterns = [
    path('add_email/', EmailAccountCreateView.as_view(), name='add_email'),
    path('messages/<int:account_id>/', EmailMessagesView.as_view() ,name='messages')
]
