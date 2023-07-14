from collections import deque
import datetime
import threading
from time import sleep

from broker.abscract_broker import AbstractBroker
from broker.broker_message.memory_broker_message import MemoryBrokerMessage


class MemoryBroker(AbstractBroker):
    __deque: dict[dict] = {}
    __deque_dead: dict[dict] = {}
    __start_tread: list[bool] = [False]

    @classmethod
    def __dead_letter_queue(cls):
        while cls.__start_tread[0]:
            for key in cls.__deque_dead:
                new_deque_dead = deque()
                while True:
                    try:
                        msg = cls.__deque_dead[key].pop()
                        if datetime.datetime.now() - msg['time'] > datetime.timedelta(seconds=1):
                            cls.__deque[key].append(msg['body'])
                        else:
                            new_deque_dead.append(msg)
                    except IndexError:
                        cls.__deque_dead[key] = new_deque_dead
                        break
            sleep(1)

    @classmethod
    def stop_thread_dead_letter(cls):
        cls.__start_tread[0] = False

    def __init__(self, name_queue):
        self.__deque[name_queue] = deque()
        self.__deque_dead[name_queue] = deque()
        self.name_queue = name_queue
        if not self.__start_tread[0]:
            self.__start_tread[0] = True
            thread = threading.Thread(target=self.__dead_letter_queue)
            thread.start()

    def push(self, msg):
        self.__deque[self.name_queue].append(msg)

    def pop(self) -> MemoryBrokerMessage | None:
        try:
            return MemoryBrokerMessage(self.__deque[self.name_queue].pop())
        except IndexError:
            return None

    def postpone_msg(self, msg):
        self.__deque_dead[self.name_queue].append({
            'time': datetime.datetime.now(),
            'body': msg.get_body(),
        })

    def cancel_msg(self, msg: MemoryBrokerMessage):
        self.__deque[self.name_queue].append(msg.get_body())

    def accept_msg(self, msg: MemoryBrokerMessage):
        msg.close()

    def close(self):
        del self.__deque[self.name_queue]
        del self.__deque_dead[self.name_queue]

    def __del__(self):
        if self.__deque.get(self.name_queue):
            self.close()
        if not self.__deque:
            self.stop_thread_dead_letter()
