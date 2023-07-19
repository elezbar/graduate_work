
import smtplib
from email.message import EmailMessage
from json import JSONDecodeError, loads
from time import sleep

from jinja2 import Template

from broker.abscract_broker import AbstractBroker
from utils.api_request import ApiRequest
from notification.email_notification import EmailNotification


class WorkerNotification:
    def __init__(
        self,
        brokers: list[AbstractBroker],
        smtp_server,
        api_request: ApiRequest,
        url_user: str,
        email_from: str
    ):
        self.brokers = brokers
        self.run_worker = True
        self.smtp_server = smtp_server
        self.api_request = api_request
        self.url_user = url_user
        self.email_from = email_from

    def stop(self):
        self.run_worker = False
        for broker in self.brokers:
            broker.close()
        self.smtp_server.close()

    def collection_data(self, msg):
        users_data = {}
        id_users = []
        for user in msg['user_data']:
            users_data[user['id_user']] = user['data']
            id_users.append(user['id_user'])
        for i in range(len(id_users)//1000+1):
            params = {
                'id_users': id_users[i*1000:(i+1)*1000]
            }
            users = self.api_request.api_call(self.url_user, params)
            for user in users:
                users_data[user['id']] = user
        return users_data

    def send_message(self, msg):
        tm = Template(msg['template'])
        cl_data = self.collection_data(msg)
        for user in cl_data:
            if msg['type_notification'] == 'email':
                msg_send = EmailNotification(cl_data[user], tm, self.smtp_server, self.email_from)
            msg_send.send_message()

    def one_itteration_job(self):
        for broker in self.brokers:
            msg_broker = broker.pop()
            if msg_broker is None:
                sleep(1)
                continue
            try:
                msg = loads(msg_broker.get_body())
                self.send_message(msg)
                broker.accept_msg(msg_broker)
            except (JSONDecodeError, smtplib.SMTPException) as e:
                broker.postpone_msg(msg_broker)
            break

    def run(self):
        while self.run_worker:
            self.one_itteration_job()
