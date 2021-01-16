from django.test import Client, TestCase

from ..services import PriorityQueue


class TestSetUp(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.client = Client()
        cls.queue = PriorityQueue()
