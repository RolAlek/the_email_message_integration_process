import email
import imaplib

from django.core.files.base import ContentFile

from .models import Attachments, EmailAccount, EmailMessage


def get_last_email(account):
    last_email = EmailMessage.objects.filter(
        email_account=account,
    ).order_by('-receive_date').first()
    if not last_email:
        return None
    return last_email


def fetch_attachment(part):
    filename = part.get_filename()
    if filename:
        filename = email.header.decode_header(filename)[0][0]

        if isinstance(filename, bytes):
            filename = filename.decode()

        attachment_data = part.get_payload(decode=True)
        attachment = Attachments()
        attachment.file.save(filename, ContentFile(attachment_data))
    return attachment


def fetch_emails_from_imap(account: EmailAccount):
    imap = imaplib.IMAP4_SSL(account.get_imap_server)
    imap.login(account.email, account.password)
    imap.select("INBOX")

    status, data = imap.search(None, 'ALL')
    email_ids = data[0].split()

    last_message = get_last_email(account)
    last_message_date = last_message.send_date if last_message else None

    result = []

    for message_id in email_ids:
        result, msg_data = imap.fetch(message_id, '(RFC822)')
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
            email_account=account,
            message_id=message_uid,
            send_date=send_date,
            subject=subject,
            text=text,
        )
        email_message.save()

        for attachment in attachments:
            attachment.message = email_message
            attachment.save()

        result.append(email_message)

    imap.close()
    imap.logout()
    return result
