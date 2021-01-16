from .setup import TestSetUp


class TicketsViewsTest(TestSetUp):
    def test_template_used(self):
        mapping = {
            '/menu/': 'menu.html',
            '/next/': 'next.html',
            '/processing': 'processing.html',
        }

        for service in self.queue.sub_queues.keys():
            mapping[f'/get_ticket/{service}/'] = 'get_ticket.html'

        for url, template in mapping.items():
            with self.subTest():
                response = self.client.get(url)
                self.assertTemplateUsed(response, template)

    def test_content(self):
        mapping = {'/welcome/': '<h2>Welcome to the Hypercar Service!</h2>'}

        for url, content in mapping.items():
            response = self.client.get(url)
            self.assertEqual(response.content.decode(), content)
