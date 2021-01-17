import json

from ..services import get_articles
from .setup import TestSetUp

from django.conf import settings


class NewsServicesTest(TestSetUp):
    def test_get_articles(self):
        super().tearDownClass()

        with self.subTest():
            self.assertEqual(get_articles(), [])

        super().setUpClass()

        with open(settings.NEWS_JSON_PATH, 'r', encoding='utf-8') as file:
            articles = json.load(file)

        with self.subTest():
            self.assertEqual(get_articles(), articles)
