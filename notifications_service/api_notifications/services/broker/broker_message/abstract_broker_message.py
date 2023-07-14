from abc import ABC, abstractmethod


class AbstractBrokerMessage(ABC):

    @abstractmethod
    def __init__(self, msg_id: str, msg_body: str):
        pass

    @abstractmethod
    def get_body(self):
        pass

    @abstractmethod
    def get_id(self):
        pass

    @abstractmethod
    def close(self):
        pass

    @abstractmethod
    def is_close(self):
        pass
