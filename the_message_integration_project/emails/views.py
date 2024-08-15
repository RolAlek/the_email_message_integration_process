from typing import Any
from django.forms import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView

from .forms import EmailAccountForm
from .models import EmailAccount


class EmailAccountCreateView(CreateView):
    model = EmailAccount
    form_class = EmailAccountForm
    template_name = 'add_email.html'

    def get_success_url(self) -> str:
        return reverse(
            'emails:messages',
            kwargs={'email_account_id': self.object.id},
        )


class EmailMessagesView(TemplateView):
    template_name = 'email_messages.html'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['email_account_id'] = self.kwargs['email_account_id']
        return context
