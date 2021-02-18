from .setup import TestSetUp


class VacancyURLsTest(TestSetUp):
    def test_exists(self):
        urls = ['/vacancies/', '/']

        for client in self.clients:
            self.check_exists(urls, client)

        urls = ['/home/']

        for client in self.authorized_clients:
            self.check_exists(urls, client)

    def test_redirects(self):
        mapping = {'/home/': '/login?next=/home/'}
        self.check_redirects(mapping, self.unauthorized_client)

    def test_not_allowed(self):
        urls = ['/vacancy/new']
        for client in self.clients:
            self.check_not_allowed(urls, client)
