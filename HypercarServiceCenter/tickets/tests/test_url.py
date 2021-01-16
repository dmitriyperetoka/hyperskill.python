from django.shortcuts import reverse

from .setup import TestSetUp


class TicketsURLsTest(TestSetUp):
    def test_exists(self):
        urls = ['/welcome/', '/menu/', '/processing', '/next/']

        for key in self.queue.sub_queues.keys():
            urls.append('/get_ticket/' + key + '/')

        for url in urls:
            with self.subTest():
                response = self.client.get(url)
                self.assertEqual(response.status_code, 200)

    def test_redirects(self):
        mapping = {'/processing/': '/processing', '/': '/menu/'}
        for url, redirect_url in mapping.items():
            with self.subTest():
                response = self.client.get(url)
                self.assertRedirects(response, redirect_url)

    def test_not_found(self):
        urls = ['/get_ticket/']
        for url in urls:
            response = self.client.get(url + 'just_some_text/')
            with self.subTest():
                self.assertEqual(response.status_code, 404)

    def test_reverse_names(self):
        mapping = {
            '/welcome/': reverse('welcome'),
            '/menu/': reverse('menu'),
            '/processing': reverse('processing'),
            '/next/': reverse('next'),
        }

        for service in self.queue.sub_queues.keys():
            mapping[f'/get_ticket/{service}/'] = reverse(
                'get_ticket', kwargs={'service': service}
            )

        for url, reverse_name in mapping.items():
            with self.subTest():
                self.assertEqual(url, reverse_name)
