

from email.message import EmailMessage
from notification.abstract_notification import AbstractNotification


class EmailNotification(AbstractNotification):

    def __init__(self, msg, template, smtp_server, email_from):
        self.tm = template
        self.smtp_server = smtp_server
        self.msg = msg
        self.email_from = email_from

    def send_message(self):
        text_email = self.tm.render(**self.msg)
        message = EmailMessage()
        message['From'] = self.email_from
        message['To'] = ",".join([self.msg['email']])
        message.add_alternative(text_email, subtype='html')
        self.smtp_server.sendmail(
            self.email_from,
            [self.email_from],
            message.as_string()
        )
