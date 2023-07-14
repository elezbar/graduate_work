import signal
import smtplib
import socket
from time import sleep


from broker.rabbit_broker import RabbitBroker
from config import config
from utils.api_request import ApiRequest
from utils.worker import WorkerNotification

worker: WorkerNotification = None


def handler_shutdown():
    worker.stop()


if __name__ == "__main__":
    brokers = [
        RabbitBroker(
            config.broker.name_instant_queue,
            config.broker.broker_login,
            config.broker.broker_password,
            config.broker.broker_host,
            config.broker.broker_port
        ),
        RabbitBroker(
            config.broker.name_delayed_queue,
            config.broker.broker_login,
            config.broker.broker_password,
            config.broker.broker_host,
            config.broker.broker_port
        )
    ]
    retry = 20
    while True:
        try:
            smtp_server = smtplib.SMTP(
                config.smtp.smtp_host,
                config.smtp.smtp_port
            )
            break
        except socket.gaierror as e:
            retry -= 1
            if retry == 0:
                raise e
            sleep(2)

    smtp_server.login(
        config.smtp.smtp_login,
        config.smtp.smtp_password
    )
    api_request = ApiRequest(
        config.broker.access_token,
    )
    worker = WorkerNotification(
        brokers,
        smtp_server,
        api_request,
        config.constants.url_get_user,
        config.constants.email_from
    )

    signal.signal(signal.SIGINT, handler_shutdown)
    signal.signal(signal.SIGTERM, handler_shutdown)
    worker.run()
