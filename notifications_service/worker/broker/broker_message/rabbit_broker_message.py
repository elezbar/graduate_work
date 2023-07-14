from .abstract_broker_message import AbstractBrokerMessage


class RabbitBrokerMessage(AbstractBrokerMessage):

    def __init__(self, msg_id: str, msg_body: str):
        self.msg_id = msg_id
        self.msg_body = msg_body
        self.__close = False

    def get_body(self):
        return self.msg_body

    def get_id(self):
        return self.msg_id

    def close(self):
        self.__close = True

    def is_close(self):
        return self.__close
