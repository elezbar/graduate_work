from abc import ABC, abstractmethod

from services.broker.broker_message.abstract_broker_message import AbstractBrokerMessage


class AbstractBroker(ABC):

    @abstractmethod
    def __init__(self, queue_name: str, login: str, password: str, host: str, port: int):
        pass

    @abstractmethod
    def push(self, msg):
        pass

    @abstractmethod
    def pop(self) -> AbstractBrokerMessage:
        pass

    @abstractmethod
    def cancel_msg(self, msg):
        pass

    @abstractmethod
    def accept_msg(self, msg):
        pass

    @abstractmethod
    def close(self):
        pass
