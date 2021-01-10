from users.tests.setup import TestClientsSetUp


class ResumeURLTest(TestClientsSetUp):
    def test_exists(self):
        urls = ['/resumes/']

        for client in self.clients:
            self.check_exists(urls, client)

    def test_not_allowed(self):
        urls = ['/resume/new']
        for client in self.clients:
            self.check_not_allowed(urls, client)
