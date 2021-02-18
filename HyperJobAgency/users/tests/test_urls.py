from vacancy.tests.setup import TestSetUp


class UsersURLsTest(TestSetUp):
    def test_exists(self):
        urls = ['/signup', '/login']
        self.check_exists(urls, self.unauthorized_client)

    def test_redirects(self):
        mapping = {'/signup/': '/signup', '/login/': '/login', '/logout/': '/'}
        self.check_redirects(mapping, self.unauthorized_client)

        mapping = {'/login': '/'}

        for client in self.authorized_clients:
            self.check_redirects(mapping, client)

    def test_redirect_chain(self):
        mapping = {'/login/': [('/login', 302), ('/', 302)]}

        for client in self.authorized_clients:
            self.check_redirect_chain(mapping, client)
