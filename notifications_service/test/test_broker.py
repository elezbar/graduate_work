import unittest

from worker.broker.memory_broker import MemoryBroker
from worker.broker.broker_message.memory_broker_message import MemoryBrokerMessage


class TestBroker(unittest.TestCase):

    def setUp(self):
        self.broker = MemoryBroker('123')

    def tearDown(self):
        self.broker.close()

    def test_push_pop(self):
        self.broker.push('test')
        msg = self.broker.pop()
        self.assertEqual(type(msg), MemoryBrokerMessage)
