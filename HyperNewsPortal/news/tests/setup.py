import json
import os

from django.conf import settings
from django.test import TestCase, override_settings

from . import fixtures


@override_settings(
    NEWS_JSON_PATH=os.path.join(
        os.path.join(
            os.path.join(settings.BASE_DIR, 'news'), 'tests'
        ),
        'news.json'
    )
)
class TestSetUp(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        with open(settings.NEWS_JSON_PATH, 'w', encoding='utf-8') as file:
            json.dump(fixtures.articles, file)

    @classmethod
    def tearDownClass(cls):
        os.remove(settings.NEWS_JSON_PATH)
