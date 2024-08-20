from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class EmailAccount(models.Model):
    PROVIDERS = [
        ('gmail.com', 'Gmail'),
        ('yandex.ru', 'Yandex'),
        ('mail.ru', 'Mail.ru'),
    ]
    IMAP_SERVERS = {
        'gmail.com': 'imap.gmail.com',
        'yandex.ru': 'imap.yandex.ru',
        'mail.ru': 'imap.mail.ru',
    }
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='email_accounts',
        null=True,
    )
    provider = models.CharField(verbose_name='Провайдер', choices=PROVIDERS)
    email = models.EmailField(verbose_name='Почта', unique=True)
    password = models.CharField(verbose_name='Пароль', max_length=128)

    @property
    def get_imap_server(self):
        return self.IMAP_SERVERS[self.provider]


class EmailMessage(models.Model):
    message_id = models.CharField(
        verbose_name='MessageID',
        max_length=128,
        unique=True,
    )
    email_account = models.ForeignKey(EmailAccount, on_delete=models.CASCADE)
    subject = models.CharField(verbose_name='Тема', max_length=256)
    send_date = models.DateTimeField(verbose_name='Дата отправки')
    receive_date = models.DateTimeField(
        verbose_name='Дата получения',
        auto_now_add=True,
    )
    text = models.TextField(verbose_name='Текст')


class Attachments(models.Model):
    message = models.ForeignKey(
        EmailMessage,
        on_delete=models.CASCADE,
        related_name='attachments',
    )
    file = models.FileField(
        verbose_name='Файл',
        upload_to='attachments/',
        blank=True,
    )
