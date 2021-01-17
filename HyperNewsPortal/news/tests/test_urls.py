from django.shortcuts import reverse

from . import fixtures
from .setup import TestSetUp


class NewsURLsTest(TestSetUp):
    def test_exists(self):
        urls = ['/news/', '/news/create/']

        for link in fixtures.links:
            urls.append(f'/news/{link}/')

        for url in urls:
            with self.subTest():
                response = self.client.get(url)
                self.assertEqual(response.status_code, 200)

    def test_redirects(self):
        mapping = {'/': '/news/'}

        for url, redirect_url in mapping.items():
            with self.subTest():
                response = self.client.get(url)
                self.assertRedirects(response, redirect_url)

    def test_not_found(self):
        urls = ['/news/']

        for url in urls:
            response = self.client.get(url + '0/')

            with self.subTest():
                self.assertEqual(response.status_code, 404)

    def test_reverse_names(self):
        mapping = {
            '/news/create/': reverse('create_article'),
            '/news/': reverse('main_page'),
            '/': reverse('index'),
        }

        for link in fixtures.links:
            mapping[f'/news/{link}/'] = reverse(
                'article_page', kwargs={'link': link}
            )

        for url, reverse_name in mapping.items():
            with self.subTest():
                self.assertEqual(url, reverse_name)
