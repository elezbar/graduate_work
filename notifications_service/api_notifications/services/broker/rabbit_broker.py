import pika

from services.broker.abscract_broker import AbstractBroker
from services.broker.broker_message.rabbit_broker_message import RabbitBrokerMessage


class RabbitBroker(AbstractBroker):
    def __init__(self,
                 queue_name: str,
                 login: str,
                 password: str,
                 host: str,
                 port: int,
                 durable: bool = True,
                 dead_timeout: int = 600):
        """
            Инициализация брокера сообщений:
            Arguments: 
                :param queue_name: Название очереди
                :type queue_name: String
                :param login: Имя пользователя
                :type login: String
                :param password: Пароль
                :type password: String
                :param host: Адрес Брокера
                :type host: String
                :param port: Порт Брокера
                :type port: Integer
                :param durable: Долговременная очередь(запись на диск)
                :type durable: Boolean
        """
        credentials = pika.PlainCredentials(login, password)
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=host,
                port=port,
                credentials=credentials,
                socket_timeout=30,
                heartbeat=0
            )
        )
        self.channel_queue = self.connection.channel()
        self.queue_name = queue_name
        self.channel_queue.exchange_declare(
            exchange=queue_name+'_excange',
            exchange_type='fanout'
        )
        self.channel_queue.exchange_declare(
            exchange='dead_'+queue_name+'_excange',
            exchange_type='fanout'
        )
        self.channel_queue.queue_declare(
            queue=queue_name,
            durable=durable,
            arguments={
                'x-dead-letter-exchange': 'dead_'+queue_name+'_excange',
            }
        )
        self.channel_queue.queue_declare(
            queue='dead_'+queue_name,
            durable=True,
            arguments={
                'x-message-ttl': dead_timeout,
                'x-dead-letter-exchange': queue_name+'_excange',
            }
        )
        self.channel_queue.queue_bind(
            exchange='dead_'+queue_name+'_excange',
            queue='dead_'+queue_name,
        )
        self.channel_queue.queue_bind(
            queue_name,
            queue_name+'_excange'
        )

    def push(self, body: str):
        """
            Отправка сообещиня в брокер
            Arguments: 
                :param body: Содержание сообщения
                :type body: String
        """
        self.channel_queue.basic_publish(exchange='',
                                         routing_key=self.queue_name,
                                         body=body,
                                         properties=pika.BasicProperties(
                                                delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
                                            )
                                        )

    def pop(self) -> RabbitBrokerMessage:
        """
            Получение сообщения из брокера
            Return: 
                :type RabbitBrokerMessage: Объект сообщения 
        """
        body = None
        method_frame, header_frame, body = self.channel_queue.basic_get(
            self.queue_name
        )
        if method_frame:
            return RabbitBrokerMessage(method_frame.delivery_tag, body.decode('utf-8'))
        return body

    def cancel_msg(self, msg: RabbitBrokerMessage):
        """
        Отмена сообщения и возврат в очередь
        Arguments: 
                :param msg: Сообщение
                :type msg: RabbitBrokerMessage
        """
        if not msg.is_close():
            msg.close()
            self.channel_queue.basic_nack(msg.get_id())

    def postpone_msg(self, msg: RabbitBrokerMessage):
        """
        Отмена сообщения и отправка dead letter queue
        Arguments:
                :param msg: Сообщение
                :type msg: RabbitBrokerMessage
        """
        if not msg.is_close():
            msg.close()
            self.channel_queue.basic_reject(
                delivery_tag=msg.get_id(),
                requeue=False
            )

    def accept_msg(self, msg: RabbitBrokerMessage):
        """
        Подтверждение сообщения и изъятие из очереди
        Arguments:
                :param msg: Сообщение
                :type msg: RabbitBrokerMessage
        """
        if not msg.is_close():
            msg.close()
            self.channel_queue.basic_ack(msg.get_id())

    def close(self):
        """
            Закрытие брокера сообщений
        """
        self.channel_queue.close()
        self.connection.close()

