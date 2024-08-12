from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView

from .forms import EmailAccountForm
from .models import EmailAccount


class EmailAccountCreateView(CreateView):
    model = EmailAccount
    form_class = EmailAccountForm
    template_name = 'add_email.html'

    def get_success_url(self) -> str:
        return reverse_lazy(
            'emails:messages',
            kwargs={'account_id': self.object.id},
        )


class EmailMessagesView(TemplateView):
    template_name = 'email_messages.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['account_id'] = self.kwargs['account_id']
        return context
