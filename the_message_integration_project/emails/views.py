from django.urls import reverse_lazy
from django.views.generic.edit import CreateView

from .forms import EmailAccountForm
from .models import EmailAccount


class EmailAccountCreateView(CreateView):
    model = EmailAccount
    form_class = EmailAccountForm
    template_name = 'add_email.html'
    success_url = reverse_lazy('emails:messages')
