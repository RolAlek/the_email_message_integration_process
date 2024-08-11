from django.urls import include, path

from .views import EmailAccountCreateView

app_name = 'emails'

urlpatterns = [
    path('add_email/', EmailAccountCreateView.as_view(), name='add_email'),
    # path('messages/', name='messages')
]
