from ..models import Resume
from users.tests.setup import TestClientsSetUp


class ResumeViewsTest(TestClientsSetUp):
    def test_template_used(self):
        mapping = {'resume_list': 'vacancy_list.html'}
        client = self.unauthorized_client
        self.check_template_used(mapping, client)

    def test_context_object_list_page(self):
        client = self.authorized_client
        reverse_name = 'resume_list'
        model = Resume
        self.check_context_object_list(client, reverse_name, model)

    def test_object_create(self):
        client = self.authorized_client
        reverse_name = 'create_resume'
        model = Resume
        self.check_object_create(client, reverse_name, model)
