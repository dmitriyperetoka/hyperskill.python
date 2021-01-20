from django.test import TestCase

from ..services import PriorityQueue


class TestSetUp(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.queue = PriorityQueue()
