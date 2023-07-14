from abc import ABC, abstractmethod


class AbstractNotification(ABC):

    @abstractmethod
    def __init__(self, msg):
        pass

    @abstractmethod
    def send_message(self):
        pass
