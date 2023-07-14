from .abstract_broker_message import AbstractBrokerMessage


class MemoryBrokerMessage(AbstractBrokerMessage):

    def __init__(self, msg_body: str):
        self.msg_body = msg_body
        self.__close = False

    def get_body(self):
        return self.msg_body

    def get_id(self):
        return None

    def close(self):
        self.__close = True

    def is_close(self):
        return self.__close
