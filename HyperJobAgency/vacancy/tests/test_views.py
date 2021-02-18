from ..forms import VacancyForm
from ..models import Vacancy
from .setup import TestSetUp
from resume.forms import ResumeForm


class VacancyViewsTest(TestSetUp):
    def test_template_used(self):
        mapping = {
            'login': 'login.html',
        }
        client = self.unauthorized_client
        self.check_template_used(mapping, client)

        mapping = {
            'signup': 'signup.html',
            'home': 'home.html',
            'vacancy_list': 'vacancy_list.html',
            'menu': 'menu.html',
        }
        for client in self.authorized_clients:
            self.check_template_used(mapping, client)

    def test_context_equal(self):
        assertion = self.assertEqual

        mapping = {
            'menu': {
                'greeting_message': 'Welcome to HyperJob!',
                'menu': [
                    'login', 'signup', 'vacancies', 'resumes', 'home', 'logout'
                ]
            }
        }

        for client in self.clients:
            self.check_context(mapping, client, assertion)

        mapping = {'home': {'object_type': 'vacancy'}}
        client = self.authorized_staff_client
        self.check_context(mapping, client, assertion)

        mapping = {'home': {'object_type': 'resume'}}
        client = self.authorized_client
        self.check_context(mapping, client, assertion)

    def test_context_is_instance(self):
        assertion = self.assertIsInstance

        mapping = {'home': {'form': VacancyForm}}
        client = self.authorized_staff_client
        self.check_context(mapping, client, assertion)

        mapping = {'home': {'form': ResumeForm}}
        client = self.authorized_client
        self.check_context(mapping, client, assertion)

    def test_context_object_list(self):
        client = self.authorized_staff_client
        reverse_name = 'vacancy_list'
        model = Vacancy
        self.check_context_object_list(client, reverse_name, model)

    def test_object_create(self):
        client = self.authorized_staff_client
        reverse_name = 'create_vacancy'
        model = Vacancy
        self.check_object_create(client, reverse_name, model)
