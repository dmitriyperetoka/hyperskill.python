import json

from . import fixtures
from .setup import TestSetUp

from django.conf import settings


class TicketsViewsTest(TestSetUp):
    def test_template_used(self):
        mapping = {
            '/news/': 'main_page.html',
            '/news/create/': 'create_article.html',
        }

        for link in fixtures.links:
            mapping[f'/news/{link}/'] = 'article_page.html'

        for url, template in mapping.items():
            with self.subTest():
                response = self.client.get(url)
                self.assertTemplateUsed(response, template)

    def test_object_list(self):
        with open(settings.NEWS_JSON_PATH, 'r', encoding='utf-8') as file:
            loaded_articles = json.load(file)

        response = self.client.get('/news/')
        self.assertEqual(response.context.get('articles'), loaded_articles)

    def test_object_create(self):
        initial_articles = self.client.get('/news/').context.get('articles')
        initial_links = [article['link'] for article in initial_articles]
        self.client.post('/news/create/', data=fixtures.new_article_kwargs)
        articles = self.client.get('/news/').context.get('articles')

        with self.subTest():
            self.assertNotIn(articles[-1]['link'], initial_links)

        with self.subTest():
            self.assertEqual(articles, initial_articles + [articles[-1]])

    def test_object_search(self):
        self.client.post('/news/create/', data=fixtures.new_article_kwargs)
        patterns = [fixtures.query_pattern_1, fixtures.query_pattern_2]

        for pattern in patterns:
            response = self.client.get('/news/', data={'q': pattern})
            articles = response.context.get('articles')

            for article in articles:
                title = article['title']
                text = article['text']

                with self.subTest():
                    self.assertTrue(pattern in title or pattern in text)

    def test_object_detail(self):
        articles = self.client.get('/news/').context.get('articles')
        assert articles, 'no articles found'

        for article in articles:
            response = self.client.get(f'/news/{article["link"]}/')

            with self.subTest():
                self.assertEqual(response.context.get('article'), article)
