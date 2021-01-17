from django.test import TestCase

from ..exceptions import PopFromEmptySubQueueError
from ..services import SubQueue


class TicketsExceptionsTest(TestCase):
    def setUp(self):
        self.sub_queue = SubQueue('Just another service', 1)

    def test_pop_from_empty_sub_queue(self):
        self.assertTrue(self.sub_queue.is_empty())

        with self.assertRaises(PopFromEmptySubQueueError):
            self.sub_queue.pop()
