import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from apiclient import errors

from common.utils.google_api_utils import GoogleApiClientGenerator


class EmailHandler:
    def __init__(self):
        self.application_name = 'Gmail API Python Send Email'

    def _create_message(self, sender, subject, to, message):
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = sender
        msg['To'] = ", ".join(to)
        msg.attach(MIMEText(message, 'plain'))
        raw = base64.urlsafe_b64encode(msg.as_bytes())
        raw = raw.decode()
        body = {'raw': raw}
        return body

    def send_message(self, sender, subject, to, msg_plain):
        service = self._setup_apps_attributes()
        message = self._create_message(sender, subject, to, msg_plain)
        self._send_message_internal(service, 'me', message)

    def _setup_apps_attributes(self):
        gmail_client = GoogleApiClientGenerator()
        gmail_client.authorize_the_apis()
        return gmail_client.gmail_service

    def _send_message_internal(self, service, user_id, message):
        try:
            message = (service.users().messages().send(userId=user_id, body=message).execute())
            print('Email Sent. Message Id: %s' % message['id'])
            return message
        except errors.HttpError as error:
            print('An error occurred: %s' % error)


if __name__ == '__main__':
    me = 'mfsi.shweta.mishra@gmail.com'
    EmailHandler().send_message(me, 'OTP verification', [me], 'Test email')
