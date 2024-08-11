import email
import imaplib
import json

from channels.generic.websocket import WebsocketConsumer

from .models import EmailAccount, EmailMessage
from .utils import get_last_email, fetch_attachment


class EmailConsumer(WebsocketConsumer):

    def connect(self):
        self.accept()

    def fetch_emails(self, email_account: EmailAccount):
        imap = imaplib.IMAP4_SSL(email_account.get_imap_server)
        imap.login(email_account.email, email_account.password)
        imap.select("INBOX")

        _, data = imap.search(None, 'ALL')
        email_ids = data[0].split()

        last_message = get_last_email(email_account)
        last_message_date = last_message.send_date if last_message else None

        for message_id in email_ids:
            _, msg_data = imap.fetch(message_id, '(RFC822)')
            msg = email.message_from_bytes(msg_data[0][1])

            if last_message_date and msg['Date'] <= last_message_date:
                continue

            message_uid = msg['Message-ID']
            send_date = email.utils.parsedate_to_datetime(msg['Date'])
            subject = email.header.decode_header(msg['Subject'])[0][0].decode()
            text = ''
            attachments = []

            if msg.is_multipart():
                for part in msg.walk():
                    content_disposition = str(part.get('Content-Disposition'))
                    if (
                        part.get_content_type() == 'text/plain'
                        and 'attachment' not in content_disposition
                    ):
                        text = part.get_payload(decode=True).decode()
                    elif 'attachment' in content_disposition:
                        attachments.append(fetch_attachment(part))

            else:
                text = msg.get_payload(decode=True).decode()

            email_message = EmailMessage.objects.create(
                email_account=email_account,
                message_id=message_uid,
                send_date=send_date,
                subject=subject,
                text=text,
            )
            email_message.save()

            for attachment in attachments:
                attachment.message = email_message
                attachment.save()

        imap.close()
        imap.logout()

    def send_progress(self, current, total):
        percentage = int((current / total) * 100)
        self.send(text_data=json.dumps({
            'progress': f'Checking email {current}/{total}',
            'percentage': percentage,
        }))

    def send_new_email(self, email_message):
        self.send(text_data=json.dumps({
            'new_email': {
                'message_id': email_message.message_id,
                'send_date': str(email_message.send_date),
                'subject': email_message.subject,
                'text': email_message.text[:50],
            }
        }))