from django.urls import reverse
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView

from .forms import EmailAccountForm
from .models import EmailAccount


class EmailAccountCreateView(CreateView):
    model = EmailAccount
    form_class = EmailAccountForm
    template_name = 'add_email.html'


    def form_valid(self, form):
        response = super().form_valid(form)
        self.request.session['email_account_id'] = self.object.id
        return response

    def get_success_url(self):
        return reverse('emails:messages')

class EmailMessagesView(TemplateView):
    template_name = 'email_messages.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        email_account_id = self.request.session.get('email_account_id')
        context['email_account_id'] = email_account_id
        return context
